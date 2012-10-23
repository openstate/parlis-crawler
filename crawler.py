#!/usr/bin/env python
# encoding: utf-8

import sys
import getopt
import datetime
import itertools
import httplib2
import os
import urllib

help_message = '''
Usage: crawer.py [-p <path>] [-a <attribute>] [-f <from_date>]
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def date_generator(from_date):
  while True:
    yield from_date
    from_date = from_date - datetime.timedelta(days=1)

h = httplib2.Http(disable_ssl_certificate_validation=True)
h.add_credentials( 'SOS', 'Open2012' )

def crawler(ingang, attribuut, datum=datetime.datetime.today()):
	datum=datetime.datetime.today()
	path = 'DutchRegents/crawler/%s/%s/%s' % (datum.date(), attribuut, ingang)
	try:
		os.makedirs(path)
	except OSError as exc:
		pass

	for x in itertools.islice(date_generator(datum), 60):
		total = 0
		path = 'DutchRegents/crawler/%s/%s/%s/%s_%d.atom.xml' % (datum.date(), attribuut, ingang, x.date(), total)
		if not os.path.exists(path):
			while True:
				f = str(x.date())
				t = str((x + datetime.timedelta(days=1)).date())
				url = 'https://api.tweedekamer.nl/APIDataService/v1/'+ingang+'/?$filter='+attribuut+'%20ge%20datetime%27'+f+'%27%20and%20'+attribuut+'%20lt%20datetime%27'+t+'%27&$skip='+str(total)
				print url
				resp, content = h.request( url, 'GET' )
				f = open(path, 'w')
				f.write(content)
				f.close()

				occurences = content.count('<entry>')
				if occurences < 250:
					break;

				total += occurences

				path = 'DutchRegents/crawler/%s/%s/%s/%s_%d.atom.xml' % (datum.date(), attribuut, ingang, x.date(), total)

def main(argv=None):
    verbose = False
    path = 'Zaken'
    attribute = 'GewijzigdOp'
    from_date = datetime.datetime.today()

    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hp:a:f:v", ["help", "path=", "attribute=", "from="])
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

        crawler(path, attribute, from_date)

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