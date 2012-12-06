#!/usr/bin/env python
# encoding: utf-8

import sys
import getopt
import datetime
import itertools
import httplib2
import os
import urllib
import logging

from parlis_utils import get_http_client
from zaken_subtree import parse_atom as parse_atom_zaken_subtree
from besluiten_stemmingen import parse_atom as parse_besluiten_stemmingen_subtree

from atomtotsv_zaken import parse_atom as convert_atom_zaken_to_tsv
from atomtotsv2_zaken import parse_zaken as convert_atom_zaken_subtree_to_tsv

from atomtotsv_besluitem import parse_atom as convert_atom_besluiten_to_tsv

h = get_http_client()

logger = logging.getLogger(__name__)

help_message = '''
Usage: crawer.py [-p <path>] [-a <attribute>] [-f <from_date>]
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def date_generator(from_date, end_date):
  while from_date <= end_date:
    yield from_date
    from_date = from_date + datetime.timedelta(days=1)

def crawler(ingang, attribuut, datum=datetime.datetime.today(), eind_datum=datetime.datetime.today()):
    for x in date_generator(datum, eind_datum):
        total = 0

        base_path = 'DutchRegents/crawler/%s/%s/%s' % (x.date(), attribuut, ingang)
        try:
            os.makedirs(base_path)
        except OSError as exc:
            pass
        
        path = '%s/%s_%d.atom.xml' % (base_path, x.date(), total)

        if not os.path.exists(path):
            while True:
                f = str(x.date())
                t = str((x + datetime.timedelta(days=1)).date())
                url = 'https://api.tweedekamer.nl/APIDataService/v1/'+ingang+'/?$filter='+attribuut+'%20ge%20datetime%27'+f+'%27%20and%20'+attribuut+'%20lt%20datetime%27'+t+'%27&$skip='+str(total)
                logger.info(url)
                resp, content = h.request( url, 'GET' )
                f = open(path, 'w')
                f.write(content)
                f.close()

                occurences = content.count('<entry>')
                if occurences < 250:
                    break;

                total += occurences

                path = 'DutchRegents/crawler/%s/%s/%s/%s_%d.atom.xml' % (x.date(), attribuut, ingang, x.date(), total)

        if ingang == 'Zaken':
            parse_atom_zaken_subtree('DutchRegents/crawler/%s/GewijzigdOp/Zaken' % (x.date()))
            convert_atom_zaken_to_tsv('DutchRegents/crawler/%s/GewijzigdOp' % (x.date()), 'Zaken')
            convert_atom_zaken_subtree_to_tsv('DutchRegents/crawler/%s/GewijzigdOp/Zaken' % (x.date()))
        elif ingang == 'Stemmingen':
            pass
        elif ingang == 'Besluiten':
            parse_besluiten_stemmingen_subtree('DutchRegents/crawler/%s/GewijzigdOp/Besluiten' % (x.date()))
            convert_atom_besluiten_to_tsv('DutchRegents/crawler/%s/GewijzigdOp' % (x.date()), 'Besluiten')
        elif ingang == 'Activiteiten':
            pass

def main(argv=None):
    verbose = False
    path = 'Zaken'
    attribute = 'GewijzigdOp'
    from_date = datetime.datetime.today()
    till_date = datetime.datetime.today()

    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hp:a:f:t:v", ["help", "path=", "attribute=", "from=", "till="])
        except getopt.error, msg:
            raise Usage(msg)

        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-p", "--path"):
                path = value.capitalize()
            if option in ("-a", "--attribute"):
                attribute = value
            if option in ("-f", "--from"):
                from_date = datetime.datetime.strptime(value, '%Y-%m-%d')
            if option in ("-t", "--till"):
                till_date = datetime.datetime.strptime(value, '%Y-%m-%d')

        crawler(path, attribute, from_date, till_date)

    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2

if __name__ == '__main__':
    #crawler('Documenten', 'Datum')
    #crawler('Stemmingen', 'GewijzigdOp')
    #crawler('Besluiten', 'GewijzigdOp')
    #crawler('Activiteiten', 'GewijzigdOp')
    #crawler('Zaken', 'GewijzigdOp')
    sys.exit(main())
