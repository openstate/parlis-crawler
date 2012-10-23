#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from lxml import etree
import os
import codecs
import iso8601
import time
import uuid
import sys
from chardet import detect
encoding = lambda x: detect(x)['encoding']

path = '/mnt/tmp/apicrawl/DutchRegents/Documenten-by-date'

for filename in sorted(os.listdir(path)):
	tree = etree.parse(path + '/' + filename)
	for elem in tree.iterfind('.//{http://www.w3.org/2005/Atom}entry'):
		guid = elem.find('.//{http://schemas.microsoft.com/ado/2007/08/dataservices}Id').text
		txtfile = '/mnt/tmp/apicrawl/DutchRegents/txt/'+guid+'.txt'
		if os.path.exists(txtfile):
			id = str(abs(hash(uuid.UUID(guid))))
			onderwerp = elem.find('.//{http://schemas.microsoft.com/ado/2007/08/dataservices}Onderwerp').text.replace('<', '').replace('>', '')
			timestamp = str(int(time.mktime(iso8601.parse_date(elem.find('.//{http://schemas.microsoft.com/ado/2007/08/dataservices}DatumRegistratie').text).timetuple())))
			contents = open(txtfile, 'r').read()
			myencoding = encoding(contents)
			if myencoding is not None:
				body = unicode(contents, myencoding, errors='ignore').encode('utf-8').decode('ascii', 'ignore').replace('<', '').replace('>', '')
				print '<document><id>'+id+'</id><timestamp>'+timestamp+'</timestamp><title>'+onderwerp[0:1022]+'</title><body>'+onderwerp+' '+body+'</body></document>'
