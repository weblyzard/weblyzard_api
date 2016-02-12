'''
Created on Oct 30, 2015

@author: lucas
'''
import logging

from random import random
from time import sleep
from weblyzard_api.client.joanna import Joanna

logger = logging.getLogger('weblyzard_api.client.joanna_argparse')

DAYS_BACK_DEFAULT = 20


def check_arguments(args):
    ''' Check the appropriate argument, give feedback on correct
    or incorrect arguments and route to the appropriate function 
    in joanna
    '''
    if args.host_url:
        jo = Joanna(url=args.host_url)
    else:
        print 'host url required..'
        return
    if args.status:
        status = jo.status()
        print 'status {}'.format(status)
    elif args.api_version:
        version = jo.version()
        print 'version: {}'.format(version)
    elif args.get_hashes:
        if None in (args.sourceId, args.portal_db):
            print "SourceId and portal_db required.."
        else:
            hashes = jo.get_hashes(args.sourceId, args.portal_db)
            print hashes
    elif args.clean_hashes:
        clean = jo.clean_hashes()
        print 'Hashes cleaned {}'.format(clean)
    elif args.reload:
        if None in (args.sourceId, args.portal_db):
            print 'invalid arguments. Requires sourceId and portal_db'
            return
        if args.repeat_test:
            for i in xrange(args.repeat_test):
                reloaded = jo.reload_source_nilsimsa(
                    args.sourceId, args.portal_db, 
                    daysBack=args.days_back)
                sleep(random()*10)
                print "Iteration {} Reloaded: {}".format(i, reloaded)
        else:
            reloaded = jo.reload_source_nilsimsa(
                   args.sourceId, args.portal_db, daysBack=args.days_back)
            print "Reloaded: {}".format(reloaded)
    elif args.send_document:
        if None in (args.sourceId, args.nilsimsa, args.portal_db):
            print 'invalid arguments. Requires sourceId, \
            portal_db and nilsimsa list..'
            return
        else:
            if args.days_back is None:
                print 'Using days back default {}'.format(
                                                    DAYS_BACK_DEFAULT)
            result = jo.similar_document(
                        args.sourceId, args.nilsimsa, args.portal_db)
            print "Result {}".format(result)
    elif args.batch_document:
        if None in (args.sourceId, args.nilsimsa_list, args.portal_db):
            print 'invalid arguments. Requires sourceId, \
            nilsimsa list and portal_db..'
            return
        else:
            if args.days_back is None:
                print 'Using days back default {}'.format(
                                                    DAYS_BACK_DEFAULT)
            result = jo.similar_documents(
                    args.sourceId, args.portal_db, args.nilsimsa_list, 
                    daysBack=args.days_back)
            print "Result {}".format(result)
    elif args.nilsimsa_list and args.batch_document is False:
        print 'need to specify --batch-document with nilsimsa-list'
    
    elif args.nilsimsa and args.send_document is False:
        print 'need to specify --send-document with a nilsimsa'


def main():
    ''' Parser for argparse. Define the command line arguments
    '''
    from argparse import ArgumentParser
    
    parser = ArgumentParser()
    parser.add_argument(
            '--host-url', dest='host_url', required=True, 
            help="Host where web service is running. \
            e.g http://localhost:8080")
    parser.add_argument('--sourceId', type=int)
    parser.add_argument('--portal-db', dest='portal_db')
    parser.add_argument('--nilsimsa', dest='nilsimsa')
    parser.add_argument(
            '--nilsimsa-list', dest='nilsimsa_list', nargs='+')
    parser.add_argument('--days-back', dest='days_back', type=int)
    parser.add_argument('--status', action='store_true')
    parser.add_argument('--api-version', dest='api_version', 
                        action='store_true')
    parser.add_argument(
                    '--reload', action='store_true', 
                    help="""load nilsimsa hashes from db.
                    Requires sourceId, portalDb, days back args""")
    parser.add_argument(
            '--get-hashes', dest='get_hashes', action='store_true')
    parser.add_argument('--clean-hashes', dest='clean_hashes', 
                        action='store_true')
    parser.add_argument(
            '--send-document', dest='send_document', 
            action='store_true', help="""send a single nilsimsa hash.
            Requires sourceId and nilsimsa""")
    parser.add_argument(
            '--batch-document', dest='batch_document', 
            action='store_true', help="""load nilsimsa hashes from db.
            Requires sourceId, portalDb, days back args""")
    parser.add_argument('--num-docs', dest='num_docs', type=int)
    parser.add_argument('--repeat-test', type=int, 
                        dest='repeat_test', help="repeat X times")
    args = parser.parse_args()
    check_arguments(args)
    
if __name__ == '__main__':    
    main()
