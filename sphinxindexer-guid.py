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

path = '/mnt/tmp/apicrawl/DutchRegents/Documenten-by-date'

for filename in sorted(os.listdir(path)):
	tree = etree.parse(path + '/' + filename)
	for elem in tree.iterfind('.//{http://www.w3.org/2005/Atom}entry'):
		guid = elem.find('.//{http://schemas.microsoft.com/ado/2007/08/dataservices}Id').text
		id = str(abs(hash(uuid.UUID(guid))))
		print guid, id
