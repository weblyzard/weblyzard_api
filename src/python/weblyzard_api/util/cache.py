#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on November 17, 2021

@author: jakob <jakob.steixner@modul.ac.at>

clone of eWRT.util.cache, licensed under GPL, original author
Albert Weichselbraun
'''
import logging

# from future import standard_library
#
# standard_library.install_aliases()
from builtins import next
from builtins import object
import redis
import pickle
from pickle import dump, load
from typing import Optional, List, Dict, Any

from gzip import GzipFile
from hashlib import sha1
from operator import itemgetter
from os import makedirs, remove, getpid, link, getenv
from os.path import exists, dirname, basename, join
from socket import gethostname
from time import time

from weblyzard_api.util.pickleIterator import WritePickleIterator, ReadPickleIterator

# (C)opyrights 2008-2015 by Albert Weichselbraun <albert@weichselbraun.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
__author__ = "Albert Weichselbraun"
__copyright__ = "GPL"

logger = logging.getLogger(__name__)

DEFAULT_REDIS_HOST = getenv('REDIS_HOST_WL_CACHING', 'localhost')
DEFAULT_REDIS_PORT = getenv('REDIS_PORT_WL_CACHING', 6379)


def get_unique_temp_file(fname): return join(dirname(fname),
                                             "_%s-%s-%d" % (basename(fname),
                                                            gethostname(),
                                                            getpid()))


class Cache(object):
    ''' An abstract class for caching functions '''

    def __init__(self, fn=None):
        self.fn = fn

    def __call__(self, *args, **kargs):
        ''' retrieves the result using self.fn as function and
            the cache.
            ::param args:     arguments
            ::param kargs:    optional keyword arguments
        '''
        assert self.fn
        return self.fetch(self.fn, *args, **kargs)

    def __delitem__(self, key):
        ''' Removes items from the cache
        ::param key: the item to remove
        '''
        raise NotImplementedError

    def fetchObjectId(self, key, fetch_function, *args, **kargs):
        ''' Fetches a object from the cache or computes it by calling the
            fetch_function.
            The key helps to determine whether the object is already in
            the cache or not.
        '''
        raise NotImplementedError

    def fetch(self, fetch_function, *args, **kargs):
        ''' Fetches a object from the cache or computes it by calling the
            fetch_function.
            The objectId is computed based on the function arguments
        '''
        raise NotImplementedError

    @staticmethod
    def getKey(*args, **kargs):
        ''' returns the key for a set of function parameters '''
        return (args, tuple(kargs.items()))

    @staticmethod
    def getObjectId(obj):
        ''' returns an identifier representing the object '''
        return sha1(repr(obj).encode("utf8")).hexdigest()


class DiskCache(Cache):
    ''' @class DiskCache
        Caches abitrary functions based on the function's arguments (fetch) or
        on a user defined key (fetchObjectId)

        @remarks
        This version of DiskCached is threadsafe
    '''

    def __init__(self, cache_dir, cache_nesting_level=0, cache_file_suffix="",
                 fn=None):
        ''' initializes the Cache object
            ::param cache_dir: the cache base directory
            ::param cache_nesting_level: optional number of nesting level (0)
            ::param cache_file_suffix: optional suffix for cache files
            ::param fn: function to cache (optional; required for directly calling the class
                          using __call__
        '''
        Cache.__init__(self, fn)
        self.cache_dir = cache_dir
        self.cache_file_suffix = cache_file_suffix
        self.cache_nesting_level = cache_nesting_level

        self._cache_hit = 0
        self._cache_miss = 0

    def fetch(self, fetch_function, *args, **kargs):
        ''' fetches the object with the given id, querying
             a) the cache and
             b) the fetch_function
            if the fetch_function is called, the functions result is saved
            in the cache

            ::param fetch_function: function to call if the result is not in the cache
            ::param args:   arguments
            ::param kargs:  optional keyword arguments

            ::returns: the object (retrieved from the cache or computed)
        '''
        objectId = self.getKey(*args, **kargs)
        return self.fetchObjectId(objectId, fetch_function, *args, **kargs)

    def __contains__(self, key):
        ''' returns whether the key is already stored in the cache '''
        cache_file = self._get_fname(self.getObjectId(key))
        return exists(cache_file)

    def __delitem__(self, key):
        ''' removes the given item from the cache '''
        cache_file = self._get_fname(self.getObjectId(key))
        remove(cache_file)

    def fetchObjectId(self, key, fetch_function, *args, **kargs):
        ''' fetches the object with the given id, querying
             * the cache and
             * the fetch_function
            if the fetch_function is called, the functions result is saved
            in the cache

            ::param key:      key to fetch
            ::param fetch_function: function to call if the result is not in the cache
            ::param args:     arguments
            ::param kargs:    optional keyword arguments

            ::returns: the object (retrieved from the cache or computed)
        '''
        cache_file = self._get_fname(self.getObjectId(key))
        if exists(cache_file):
            #
            # case 1: cache hit - return the cached result
            #
            self._cache_hit += 1
            with GzipFile(cache_file) as f:
                # return load(f)
                return load(f,
                            encoding='utf-8')  # [mig] FIXME: no hardcoded enc!

        #
        # case 2: cache miss
        # - compute and cache the result
        #
        temp_file = get_unique_temp_file(cache_file)

        self._cache_miss += 1
        obj = fetch_function(*args, **kargs)

        # Do not cache None
        if obj is None:
            return obj

        with GzipFile(temp_file, "w") as f:
            dump(obj, f)

        try:
            link(temp_file, cache_file)
        # ignore file exists errors
        except OSError as e:
            if e.errno != 17:
                raise e

        remove(temp_file)
        return obj

    def _remove(self, fname):
        ''' removes the given files (if it exists) '''
        try:
            remove(fname)
        except OSError:
            pass

    def getCacheStatistics(self):
        ''' returns statistics regarding the cache's hit/miss ratio '''
        return {'cache_hits': self._cache_hit, 'cache_misses': self._cache_miss}

    def _get_fname(self, obj_id):
        ''' Computes the filename of the file with the given
            object identifier and creates the required directory
            structure (if necessary).

            @returns the full path of the given object's cache file
        '''
        assert len(obj_id) >= self.cache_nesting_level

        obj_dir = join(
            *([self.cache_dir] + list(obj_id[:self.cache_nesting_level])))
        if not exists(obj_dir):
            try:
                makedirs(obj_dir)
            except OSError:  # required for multithreading
                pass

        return join(obj_dir, obj_id + self.cache_file_suffix)


class DiskCached(object):
    ''' Decorator based on Cache for caching arbitrary function calls
        usage:
          @DiskCached("./cache/myfunction")
          def myfunction(*args):

        @remarks
        This version of DiskCached is threadsafe
    '''
    __slots__ = ('cache',)

    def __init__(self, cache_dir, cache_nesting_level=0, cache_file_suffix=""):
        ''' initializes the Cache object
            ::param fn:                  the function to cache
            ::param cache_dir:           the cache base directory
            ::param cache_nesting_level: optional number of nesting level (0)
            ::param cache_file_suffix:   optional suffix for cache files
        '''
        self.cache = DiskCache(
            cache_dir, cache_nesting_level, cache_file_suffix)

    def __call__(self, fn):
        self.cache.fn = fn
        return self.cache


class MemoryCache(Cache):
    '''
        @class MemoryCached

        Caches abitrary functions based on the function's arguments (fetch) or
        on a user defined key (fetchObjectId)
    '''
    __slots__ = ('max_cache_size', '_cacheData', '_usage')

    def __init__(self, max_cache_size=0, fn=None):
        ''' initializes the Cache object '''
        Cache.__init__(self, fn)
        self._cacheData = {}
        self._usage = {}
        self.max_cache_size = max_cache_size

    def fetch(self, fetch_function, *args, **kargs):
        key = self.getKey(*args, **kargs)
        return self.fetchObjectId(key, fetch_function, *args, **kargs)

    def fetchObjectId(self, key, fetch_function, *args, **kargs):
        # update the object's last usage time stamp
        key = self.getObjectId(key)
        self._usage[key] = time()
        try:
            return self._cacheData[key]
        except KeyError:
            return self.fetch_with_fetch_function(key, fetch_function, *args, **kargs)

    def fetch_with_fetch_function(self, key, fetch_function, *args, **kargs):
        obj = fetch_function(*args, **kargs)
        if obj != None:
            self.garbage_collect_cache()
            self._cacheData[key] = obj
        return obj

    def __contains__(self, key):
        ''' returns whether the key is already stored in the cache '''
        return self.getObjectId(key) in self._cacheData

    def __delitem__(self, key):
        ''' removes the given item from the cache '''
        del self._cacheData[self.getObjectId(key)]

    def garbage_collect_cache(self):
        ''' removes the object which have not been in use for the
            longest time '''
        if self.max_cache_size == 0 or len(
                self._cacheData) <= self.max_cache_size:
            return

        (key, _) = sorted(list(self._usage.items()),
                          key=itemgetter(1), reverse=True).pop()
        del self._usage[key]
        del self._cacheData[key]


class MemoryCached(MemoryCache):
    ''' Decorator based on MemoryCache for caching arbitrary function calls
        usage:
          @MemoryCached or @MemoryCached(max_cache_size)
          def myfunction(*args):            ...
    '''

    def __init__(self, arg):
        """initializes the MemoryCache object
            ::param arg: either the max_cache_size or the function to call
        """
        if hasattr(arg, '__call__'):
            MemoryCache.__init__(self)
            self._fn = arg
        else:
            MemoryCache.__init__(self, max_cache_size=arg)
            self._fn = None

    def __call__(self, *args, **kargs):
        if self._fn is None:
            fn = args[0]

            def wrapped_fn(*args, **kargs):
                return self.fetch(fn, *args, **kargs)

            return wrapped_fn
        else:
            return self.fetch(self._fn, *args, **kargs)


class TTLMemoryCached(MemoryCached):
    """Decorator based on Memory cache for caching function calls with
    a specified time to live, results older than which will be ignored
    """

    def __init__(self, ttl, max_cache_size=0):
        MemoryCache.__init__(self, max_cache_size=max_cache_size)
        self._fn = None
        self.ttl = ttl.total_seconds()
        self._last_updated = {}

    def fetchObjectId(self, key, fetch_function, *args, **kargs):
        # update the object's last usage time stamp
        key = self.getObjectId(key)
        self._usage[key] = time()
        try:
            stored_result = self._cacheData[key]
            valid_from = self._last_updated[key]
            if time() - valid_from <= self.ttl:
                return self._cacheData[key]
            else:
                del self._usage[key]
                del self._cacheData[key]
                del self._last_updated[key]
                raise KeyError
        except KeyError:
            obj = fetch_function(*args, **kargs)
            if obj != None:
                self.garbage_collect_cache()
                self._cacheData[key] = obj
                self._last_updated[key] = time()
            return obj


class IterableCache(DiskCache):
    ''' caches arbitrary iterable content identified by an identifier '''

    def __iter__(self):
        return self

    def fetchObjectId(self, key, function, *args, **kargs):
        ''' fetches the object with the given id, querying
             a) the cache and
             b) the function
            if the function is called, the functions result is saved
            in the cache

            ::param key:      key to fetch
            ::param function: function to call if the result is not in the cache
            ::param args:     arguments
            ::param kargs:    optional keyword arguments

            ::returns: the object (retrieved from the cache or computed)
        '''
        cache_file = self._get_fname(self.getObjectId(key))

        if exists(cache_file):
            self._cached = True
            self._pickle_iterator = ReadPickleIterator(cache_file)
        else:
            self._fetch_function_iterator = function(*args, **kargs).__iter__()
            self._cached = False
            self._pickle_iterator = WritePickleIterator(cache_file)

        return self

    def __next__(self):
        return self._read_next_element() if self._cached else self._cache_next_element()

    def _cache_next_element(self):
        ''' a) retrieves the next element from the fetch function
            b) writes the data to the cache
            c) passes the data through to the calling element
        '''
        self._cache_miss += 1
        try:
            obj = next(self._fetch_function_iterator)
            self._pickle_iterator.dump(obj)
            return obj
        except StopIteration:
            self._pickle_iterator.close()
            raise StopIteration

    def _read_next_element(self):
        ''' returns the next element from the cache '''
        self._cache_hit += 1
        try:
            return next(self._pickle_iterator)
        except IOError:
            self._pickle_iterator.close()
            raise StopIteration


class RedisCache(Cache):

    def __init__(self, max_cache_size=0, fn=None, host=DEFAULT_REDIS_HOST,
                 port=DEFAULT_REDIS_PORT,
                 db=0):
        ''' initializes the Cache object '''
        Cache.__init__(self, fn)
        self._cacheData = redis.StrictRedis(host=host, port=port, db=db)
        self._usage = redis.StrictRedis(host=host, port=port, db=1)
        try:
            self._cacheData.ping()
            self.max_cache_size = max_cache_size
        except:
            print("RedisCache requires a running Redis server.")

    def fetch(self, fetch_function, *args, **kargs):
        key = self.getKey(*args, **kargs)
        return self.fetchObjectId(key, fetch_function, *args, **kargs)

    def fetchObjectId(self, key, fetch_function, *args, **kargs):
        # update the object's last usage time stamp
        key = self.getObjectId(key)
        self._usage[key] = time()
        # pickling is necessary because Redis turns every input into
        # a string
        try:
            return (pickle.loads(self._cacheData[key]))
        except KeyError:
            obj = fetch_function(*args, **kargs)
            if obj != None:
                self.garbage_collect_cache()
                p_obj = pickle.dumps(obj)
                self._cacheData[key] = p_obj
            return (obj)

    def garbage_collect_cache(self):
        ''' removes the object which have not been in use for the
            longest time '''
        if self.max_cache_size == 0 or self._cacheData.dbsize() < self.max_cache_size:
            return
        usage_dict = {k: self._usage[k] for k in list(self._usage.keys())}
        (key, _) = sorted(list(usage_dict.items()),
                          key=itemgetter(1), reverse=True).pop()
        del self._usage[key]
        del self._cacheData[key]


class RedisCached(RedisCache):
    ''' Decorator based on MemoryCache for caching arbitrary function calls
        usage:
          @MemoryCached or @MemoryCached(max_cache_size)
          def myfunction(*args):            ...
    '''

    def __init__(self, arg):
        ''' initializes the RedisCache object
            ::param arg: either the max_cache_size or the function to call
        '''
        if hasattr(arg, '__call__'):
            RedisCache.__init__(self)
            self._fn = arg
        else:
            RedisCache.__init__(self, **arg)
            self._fn = None

    def __call__(self, *args, **kargs):
        if self._fn is None:
            fn = args[0]

            def wrapped_fn(*args, **kargs):
                return self.fetch(fn, *args, **kargs)

            return wrapped_fn
        else:
            return self.fetch(self._fn, *args, **kargs)


class HybridMemoryCached(MemoryCached):

    def __init__(self, key: str, max_cache_size: int=0,
                 group: Optional[List]=None):
        MemoryCache.__init__(self, max_cache_size=max_cache_size)
        self.key = key
        self._fn = None
        self.group: List[HybridMemoryCached] = group
        self.register()
        self._dirty = set()

    def register(self):
            """register """
            self.group.append(self)

    def fetch_with_fetch_function(self, key, fetch_function, *args, **kargs):
        self._dirty.add(key)
        return MemoryCached.fetch_with_fetch_function(self,
            key, fetch_function, *args, **kargs
        )

    def sync_upstream(self, priority='local', bulk_write=False):
        raise NotImplementedError


# default group for hybrid caches - allows simultaneous updates with
# `update_hybrid_cache_group` below
REDIS_CACHE_BATCH = []


class HybridMemRedisCached(HybridMemoryCached):
    """
    A MemoryCached object that, instead of starting out with an empty slate,
    pulls its initial state from Redis, and comes with a method to
    synchronize memory content and remote data
    """

    def __init__(self, key: str, host: str=DEFAULT_REDIS_HOST,
                 port: int=DEFAULT_REDIS_PORT, max_cache_size: int=0,
                 group: Optional[List]=None):
        group = group if group is not None else REDIS_CACHE_BATCH
        HybridMemoryCached.__init__(self, max_cache_size=max_cache_size,
                                    key=key, group=group)
        self.redis = redis.StrictRedis(host=host, port=port)
        self._cacheData = self.decode_cache_data()

    def decode_cache_data(self):
        """load redis data, unpickle values, convert keys from bytes to str"""
        try:
            cache_data: Dict[bytes, Any] = {k.decode(): pickle.loads(v) for k, v in
                self.redis.hgetall(self.key).items()
            }
        except Exception as e:
            logger.warning('Unable to load data from Redis. This *may* be '
                        'expected on first instantiation, or it could be '
                        'a configurtion issue', exc_info=True)
            cache_data = {}
        return cache_data

    def redis_set_value(self, key, value):
        """write an individual key-value pair to our mapping"""
        self.redis.hset(self.key, key, pickle.dumps(value))

    def sync_upstream(self, priority: str='local',
                      bulk_write: bool=False) -> None:
        """
        synchronize current memory content with server-side data, should
        ideally be implemented as a scheduled task, or a task performed after
        certain trigger events
        :param priority: 'local' or 'server': 'local means that new data
            on the server since initialization are overwritten by what
            we have locally in case of conflicts
        :param bulk_write: write only "dirty" keys one by one when `False`
            write entire cache_data at once when `True`
        :return:
        """
        upstream_data = self.decode_cache_data()
        if priority == 'local':
            upstream_data.update(self._cacheData)
        self._cacheData.update(upstream_data)
        upstream_data.update(self._cacheData)
        if bulk_write:
            self.redis.hmset(
                self.key,
                {k: pickle.dumps(v) for k, v in upstream_data.items()}
            )
        else:
            for k in self._dirty:
                try:
                    v = self._cacheData[k]
                    self.redis_set_value(k, v)
                except KeyError:
                    continue
            self._dirty = set()


class RealtimeRedisMemCached(HybridMemRedisCached):

    def fetch_with_fetch_function(self, key, fetch_function, *args, **kargs):
        obj = fetch_function(*args, **kargs)
        if obj != None:
            self.garbage_collect_cache()
            self._cacheData[key] = obj
            self.redis_set_value(key, obj)
        return obj


DISK_CACHE_BATCH = []


class HybridMemDiskCached(HybridMemoryCached):
    """Hybrid Cache with memory caching for fast access and disk caching
    of the entire `_cacheData` as a backup for sharing between processes"""

    def __init__(self, key: str, max_cache_size: int=0,
                 group: Optional[List]=None,
                 cache_dir_path: str='/opt/weblyzard/cache'):
        group = group if group is not None else DISK_CACHE_BATCH
        HybridMemoryCached.__init__(self, max_cache_size=max_cache_size,
                                    key=key, group=group)
        self.cache_dir_path = cache_dir_path
        self.cache_file_name = f'{self.cache_dir_path}/{self.key}.pkl'
        try:
            with GzipFile(f'{self.cache_file_name}') as f:
                self._cacheData = load(f)
        except Exception as e:
            logger.warn('No disk cached data found during initialization,'
                        'this is expected at first instantiation',
                        exc_info=True)
            self._cacheData = {}

    def sync_upstream(self, priority: str='local',
                      bulk_write: bool=True) -> None:
        """
        synchronize current memory content with disk-cached data, should
        ideally be implemented as a scheduled task, or a task performed after
        certain trigger events
        :param priority: 'local' or 'server': 'local means that new data
            on the server since initialization are overwritten by what
            we have locally in case of conflicts
        :param bulk_write: for compatibility only, disk caching does not allow
            filtering for dirty keys
        :return:
        """
        try:
            with GzipFile(self.cache_file_name) as f:
                upstream_data = pickle.load(f)
        except Exception as e:
            logger.info(e, exc_info=True)
            upstream_data = {}
        if priority == 'local':
            upstream_data.update(self._cacheData)
        self._cacheData.update(upstream_data)
        upstream_data.update(self._cacheData)
        with GzipFile(self.cache_file_name, 'w') as f:
            pickle.dump(self._cacheData, f)


def update_hybrid_cache_group(
        cache_group: Optional[List[HybridMemoryCached]]=None,
        priority: str='local', bulk_write: bool=False) -> None:
    """synchronize all hybrid caches registered as part of a group of caches.
    Defaults to synchronizing all HybridCaches (Disk and Redis backed up)
    in their respective default groups"""
    if not cache_group:
        cache_group = REDIS_CACHE_BATCH + DISK_CACHE_BATCH
    for cache in cache_group:
        try:
            cache.sync_upstream(priority=priority, bulk_write=bulk_write)
        except Exception as e:
            logger.info(e, exc_info=True)
