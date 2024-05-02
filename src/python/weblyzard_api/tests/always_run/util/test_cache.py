#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on May 29, 2020

@author: jakob <jakob.steixner@modul.ac.at>
cloned from eWRT
'''
import time
import datetime
import mock
import pytest
import unittest
import os
import pickle
import redis

from gzip import GzipFile
from multiprocessing import Pool
from shutil import rmtree
from os.path import exists, join

from weblyzard_api.util.module_path import get_resource
from weblyzard_api.util.cache import (MemoryCache, MemoryCached, DiskCached,
                                      DiskCache, Cache, IterableCache,
                                      RedisCached, TTLMemoryCached,
                                      HybridMemDiskCached, DISK_CACHE_BATCH,
                                      update_hybrid_cache_group,
                                      HybridMemRedisCached, DEFAULT_REDIS_PORT,
                                      DEFAULT_REDIS_HOST, logger,
                                      RealtimeRedisMemCached)

get_cache_dir = lambda no: get_resource(__file__, ('.unittest-temp%d' % (no),))


class TestCached(unittest.TestCase):
    ''' tests the MemoryCached Decorator '''

    @staticmethod
    def add(a=2, b=3):
        return a + b

    @staticmethod
    def sub(a=2, b=3):
        return a - b

    def testNonKeywordArguments(self):
        ''' tests the class with non Keyword Arguments '''
        for x in range(1, 20):
            assert self.add(x, 5) == (x + 5)
            assert self.add(x, 5) == (x + 5)

        # test objects with a cachesize specified
        for x in range(1, 20):
            assert self.sub(x, 5) == x - 5
            assert self.sub(x, 5) == x - 5

    def testContainsDel(self):
        ''' tests the contains and del functions '''
        d = MemoryCache()
        d.fetchObjectId("10", self.add, *(), **{'a': 3, 'b': 4})
        assert "10" in d
        del d["10"]
        assert "10" not in d

    def testKeywordArguments(self):
        ''' tests keyword arguments '''
        assert self.add(3, b=7) == 3 + 7
        assert self.add(3, b=7) == 3 + 7
        assert self.add(a=9, b=8) == 9 + 8


class TestMemoryCached(TestCached):

    @staticmethod
    @MemoryCached
    def add(a=1, b=2):
        return a + b

    @staticmethod
    @MemoryCached(12)
    def sub(a=2, b=1):
        return a - b

    # todo: failing


class SkipTestDiskCached(TestCached):

    @staticmethod
    @DiskCached(get_cache_dir(1))
    def add(a=1, b=2):
        return a + b

    @staticmethod
    @DiskCached(get_cache_dir(2))
    def sub(a, b):
        return a - b

    def setUp(self):
        self.diskCache = DiskCache(get_cache_dir(4))

    def tearDown(self):
        ''' remove the cache directories '''
        for cacheDirNo in range(10):
            if exists(get_cache_dir(cacheDirNo)):
                rmtree(get_cache_dir(cacheDirNo))

    def testObjectKeyGeneration(self):
        ''' ensures that the diskcache object's location does not change '''
        CACHE_DIR = get_cache_dir(3)
        d = DiskCache(CACHE_DIR)
        getCacheLocation = lambda x: join(CACHE_DIR, Cache.getObjectId(x))

        d.fetchObjectId(1, str, 1)
        assert exists(getCacheLocation(1))

        d.fetch(str, 2)
        assert exists(getCacheLocation(((2,), ())))

    def testContains(self):
        ''' verifies that 'key' in cache works '''
        # diskcache
        assert self.diskCache.fetchObjectId(1, str, 1) == "1"

        assert 1 in self.diskCache
        assert 2 not in self.diskCache

        # diskcached
        assert self.add(12, 14) == 26
        assert self.add.getKey(12, 14) in self.add
        assert 9 not in self.add

    def testDelItem(self):
        ''' verifies that delitem works '''
        # diskcache
        assert self.diskCache.fetch(str, 2) == "2"
        key = self.diskCache.getKey(2)
        assert key in self.diskCache
        del self.diskCache[key]
        assert key not in self.diskCache

        # diskcached
        assert self.add(12, 13) == 25
        key = self.add.getKey(12, 13)
        assert key == ((12, 13), ())
        assert key in self.add
        del self.add[key]
        assert key not in self.add

    def testDirectCall(self):
        ''' tests directly calling the cache object using __call__ '''
        CACHE_DIR = get_cache_dir(4)
        cached_str = DiskCache(CACHE_DIR, fn=str)

        assert cached_str(7) == "7"
        assert cached_str.getKey(7) in cached_str

    def testIterableCache(self):
        ''' tests the iterable cache '''
        CACHE_DIR = get_cache_dir(5)
        i = IterableCache(CACHE_DIR)

        getTestIterator = lambda x: list(range(x))

        for iteratorSize in (4, 5, 6):
            cachedIterator = i.fetch(getTestIterator, iteratorSize)

            for x, y in zip(cachedIterator, getTestIterator(iteratorSize)):
                assert x == y

    @pytest.mark.slow
    def testThreadSafety(self):
        '''  tests whether everything is thread safe '''

        for a in range(1000):
            c = DiskCache(get_cache_dir(6))
            p = Pool(12)

            p.map(f, 60 * [c])
            p.map(g, 60 * [c])

            p.close()
            p.join()


def f(c):
    ''' Function for checking Diskcache with larger files.

        @remarks
        required for the testThreadSafety unittest.
        considers None results.
    '''
    from random import randint
    r = randint(1, 17)
    blow = lambda x: x not in (7, 8) and 100000 * str(x) or None
    assert c.fetch(blow, r) == blow(r)
    return 0


def g(c):
    ''' Function for checking DiskCache with small files.

        @remarks
        required for the testThreadSafety unittest.
        considers None results.
    '''

    from random import randint
    r = randint(111, 117)
    assert c.fetch(str, r) == str(r)
    return 0


args = {'host': 'localhost', 'port': 6379, 'max_cache_size': 10}


@RedisCached(args)
def dummy_function(dummy_input):
    x = 0
    for i in range(100000000):
        x = i
    print(x)
    return (x)


@RedisCached(args)
def dummy_return_dict(dummy_input):
    return ({'one': 1, 'two': 2})


@RedisCached(args)
def num_to_string(n):
    return (str(n))


@pytest.mark.skip("requires local redis instance running")
class TestRedisCache(unittest.TestCase):

    def test_int_type_preservation(self):
        x = dummy_function(1)
        assert (isinstance(x, int))

    def test_dict_type_preservation(self):
        d = dummy_return_dict(2)
        assert (isinstance(d, dict))


class TestTTLMemoryCached(unittest.TestCase):

    def test_fast_expiry(self):

        fn = mock.MagicMock(return_value=1)

        @TTLMemoryCached(ttl=datetime.timedelta(milliseconds=1))
        def dummy_fast_expiry():
            fn()

        dummy_fast_expiry()
        time.sleep(0.1)
        dummy_fast_expiry()
        assert fn.call_count == 2

    def test_slow_expiry(self):

        fn = mock.MagicMock(return_value=1)

        @TTLMemoryCached(ttl=datetime.timedelta(days=1))
        def dummy_slow_expiry():
            return fn()

        dummy_slow_expiry()
        time.sleep(0.1)
        dummy_slow_expiry()
        assert fn.call_count == 1


class TestHybridMemDiskCached():

    def test_hybrid_disk_cache(self):

        def g_(param):
            return param

        mocked_g = mock.MagicMock()
        mocked_g.return_value = 1
        # cleanup potential cache files from previous runs
        try:
            os.remove('/tmp/test_disk_cache_function.pkl')
        except:
            pass
        test_caches = []

        @HybridMemDiskCached('test_disk_cache_function', cache_dir_path='/tmp',
                             group=test_caches)
        def test_function(param):
            g_ = mocked_g
            return g_(1)

        assert not os.path.exists('/tmp/test_disk_cache_function.pkl')
        # run once, don't synchronize: expected result: 1 call to mock,
        # no cache file
        test_function(1)
        assert not os.path.exists('/tmp/test_disk_cache_function.pkl')
        mocked_g.assert_called_with(1)
        mocked_g.assert_called_once()
        # call again with the same params: expected result: still only one call
        # to nested function
        test_function(1)
        mocked_g.assert_called_once()
        test_function(2)
        assert mocked_g.call_count == 2
        # demonstrate that updating default cache group has no effect when
        # specific cache group has been assigned
        update_hybrid_cache_group(DISK_CACHE_BATCH)
        assert not os.path.exists('/tmp/test_disk_cache_function.pkl')
        # demonstrate synchronization
        update_hybrid_cache_group(test_caches)
        assert os.path.exists('/tmp/test_disk_cache_function.pkl')
        with GzipFile('/tmp/test_disk_cache_function.pkl') as f:
            assert len(pickle.load(f)) == 2


def redis_is_live():
        from weblyzard_api.util.cache import DEFAULT_REDIS_PORT, \
            DEFAULT_REDIS_HOST
        try:
            return redis.StrictRedis(
                port=DEFAULT_REDIS_PORT, host=DEFAULT_REDIS_HOST
            ).ping()
        except Exception as e:
            return False


class TestHybridMemRedisCache():

    @pytest.mark.skipif(
        not redis_is_live(),
        reason=f'No redis server available at '
               f'{DEFAULT_REDIS_HOST}:{DEFAULT_REDIS_PORT}'
    )
    def test_hybrid_redis_cache(self):

        def g_(param):
            return param

        redis_instance = redis.StrictRedis(host=DEFAULT_REDIS_HOST,
                                           port=DEFAULT_REDIS_PORT)

        mocked_g = mock.MagicMock()
        mocked_g.return_value = 1
        redis_test_caches = []
        try:
            redis_instance.delete('test_redis_cache_function')
        except Exception as e:
            logger.warning(e, exc_info=True)
        for k in redis_instance.hkeys('test_redis_cache_function'):
            redis_instance.hdel('test_redis_cache_function', k)

        @HybridMemRedisCached(key='test_redis_cache_function')
        def test_function_1(input):
            return mocked_g(input)

        assert test_function_1(1) == 1
        mocked_g.assert_called_with(1)
        mocked_g.assert_called_once()

        mocked_g.assert_called_once()
        mocked_h = mock.MagicMock()
        mocked_h.return_value = 2

        # Two different functions using the same global key - do not do this
        # at home! (here it serves to simulate two workers retrieving data
        # independently)
        @HybridMemRedisCached(key='test_redis_cache_function', group=redis_test_caches)
        def test_function_2(input):
            return mocked_h(input)

        assert test_function_2(1) == 2
        update_hybrid_cache_group()
        assert test_function_2(1) == 2
        assert test_function_1(1) == 1
        cached = HybridMemRedisCached(
            key='test_redis_cache_function').decode_cache_data()
        assert cached == {
            HybridMemRedisCached.getObjectId(
                HybridMemRedisCached.getKey(1)): 1
        }
        assert test_function_1(1) == 1
        update_hybrid_cache_group(redis_test_caches)
        update_hybrid_cache_group(priority='global')
        assert test_function_1(1) == 2
        cached = HybridMemRedisCached(
            key='test_redis_cache_function').decode_cache_data()
        assert cached == {
            HybridMemRedisCached.getObjectId(
                HybridMemRedisCached.getKey(1)): 2
        }

    @pytest.mark.skipif(
        not redis_is_live(),
        reason=f'No redis server available at '
               f'{DEFAULT_REDIS_HOST}:{DEFAULT_REDIS_PORT}'
    )
    @pytest.mark.slow
    def test_hybrid_redis_cache_performance(self):
        """Compare runtimes of hybrid redis cache with realtime
        writing vs. writing only as part of update method."""

        inputs = list(range(100000))

        def add_one(n):
            return n + 1

        print('Runtime no caching')
        start_time_no_caching = time.time()
        for i in inputs:
            a = add_one(i)
        print(time.time() - start_time_no_caching)
        # 0.011200189590454102 with 100k

        print('Write time to local redis cache with delayed writing, dirty keys only')
        redis_instance = redis.StrictRedis(host=DEFAULT_REDIS_HOST,
                                           port=DEFAULT_REDIS_PORT)
        try:
            redis_instance.delete('test_hybrid_redis_performance')
        except Exception as e:
            logger.warning(e, exc_info=True)
        hybrid_bulk_caches = []

        @HybridMemRedisCached('test_hybrid_redis_performance',
                              group=hybrid_bulk_caches)
        def test_function_bulk(n):
            return n + 1

        start_time_bulk = time.time()
        for i in inputs:
            a = test_function_bulk(i)
        print(f'time for calculations only: {time.time() - start_time_bulk}')
        # 0.7149114608764648 for mem caching without redis write (100k entries)
        update_hybrid_cache_group(hybrid_bulk_caches, bulk_write=False)
        print(f'time for calculations + writing/fetching upstream: '
              f'{time.time() - start_time_bulk}')
        cached = HybridMemRedisCached(
            key='test_hybrid_redis_performance').decode_cache_data()
        assert cached == {
            HybridMemRedisCached.getObjectId(
                HybridMemRedisCached.getKey(i)): i + 1 for i in inputs
        }
        time.sleep(10)
        extra_inputs = list(range(-10, 0))
        for i in extra_inputs:
            a = test_function_bulk(i)

        start_time_bulk_extras = time.time()
        update_hybrid_cache_group(hybrid_bulk_caches, bulk_write=False)
        print(
            f'time for writing/fetching with few updates: '
            f'{time.time() - start_time_bulk_extras}')

        time.sleep(10)
        cached = HybridMemRedisCached(
            key='test_hybrid_redis_performance').decode_cache_data()
        assert cached == {
            HybridMemRedisCached.getObjectId(
                HybridMemRedisCached.getKey(i)): i + 1 for i in inputs + extra_inputs
        }

        print('Write time to local redis cache with delayed writing, bulk method')
        redis_instance = redis.StrictRedis(host=DEFAULT_REDIS_HOST,
                                           port=DEFAULT_REDIS_PORT)
        try:
            redis_instance.delete('test_hybrid_redis_performance')
        except Exception as e:
            logger.warning(e, exc_info=True)
        hybrid_bulk_caches = []

        start_time_bulk = time.time()
        for i in inputs:
            a = test_function_bulk(i)
        print(f'time for calculations only: {time.time() - start_time_bulk}')
        update_hybrid_cache_group(hybrid_bulk_caches, bulk_write=True)
        print(f'time for calculations + writing/fetching upstream: {time.time() - start_time_bulk}')

        time.sleep(10)
        cached = HybridMemRedisCached(
            key='test_hybrid_redis_performance').decode_cache_data()
        assert cached == {
            HybridMemRedisCached.getObjectId(
                HybridMemRedisCached.getKey(i)): i + 1 for i in inputs
        }

        time.sleep(10)
        extra_inputs = list(range(-10, 0))
        for i in extra_inputs:
            a = test_function_bulk(i)

        start_time_bulk_extras = time.time()
        update_hybrid_cache_group(hybrid_bulk_caches, bulk_write=True)
        print(
            f'time for writing/fetching with few updates: {time.time() - start_time_bulk_extras}')

        time.sleep(10)
        cached = HybridMemRedisCached(
            key='test_hybrid_redis_performance').decode_cache_data()
        assert cached == {
            HybridMemRedisCached.getObjectId(
                HybridMemRedisCached.getKey(i)): i + 1 for i in inputs + extra_inputs
        }

        time.sleep(10)
        try:
            redis_instance.delete('test_hybrid_redis_performance')
        except Exception as e:
            logger.warning(e, exc_info=True)

        time.sleep(10)
        cached = HybridMemRedisCached(
            key='test_hybrid_redis_performance').decode_cache_data()
        assert cached == {}

        time.sleep(10)
        hybrid_realtime_caches = []
        print('write time to local realtime hybrid redis cache')

        @RealtimeRedisMemCached('test_hybrid_redis_performance', group=hybrid_realtime_caches)
        def test_function_realtime(n):
            return n + 1

        start_time_rt = time.time()
        for i in inputs:
            a = test_function_realtime(i)
        print(f'time for calculations only: {time.time() - start_time_rt}')
        update_hybrid_cache_group(hybrid_realtime_caches)
        print(f'time for calculations + fetching upstream: {time.time() - start_time_rt}')

        time.sleep(10)
        cached = HybridMemRedisCached(
            key='test_hybrid_redis_performance').decode_cache_data()
        assert cached
        assert cached == {
            HybridMemRedisCached.getObjectId(
                HybridMemRedisCached.getKey(i)): i + 1 for i in inputs
        }

        time.sleep(10)
        start_time_rt = time.time()
        for i in inputs:
            a = test_function_realtime(i)
        print(f'time for calculations only (seen inputs): {time.time() - start_time_rt}')
        update_hybrid_cache_group(hybrid_realtime_caches)
        print(f'time for calculations + fetching upstream (w/o new inputs): {time.time() - start_time_rt}')

        cached = HybridMemRedisCached(
            key='test_hybrid_redis_performance').decode_cache_data()
        assert cached
        assert cached == {
            HybridMemRedisCached.getObjectId(
                HybridMemRedisCached.getKey(i)): i + 1 for i in inputs
        }
