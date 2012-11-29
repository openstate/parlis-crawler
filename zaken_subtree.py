#!/usr/bin/env python

import sys
import os
import codecs
import httplib2
import datetime
from lxml import etree

from parlis_utils import get_http_client

h = get_http_client()

def parse_atom(path):
	for subtree in ['ZaakActoren', 'Statussen', 'KamerstukDossier', 'Documenten', 'Activiteiten', 'Besluiten', 'GerelateerdVanuit', 'GerelateerdNaar', 'HoofdOverig', 'GerelateerdOverig', 'VervangenVanuit', 'VervangenDoor', 'Agendapunten']:
		try:
			os.mkdir(path+'_'+subtree)
		except:
			pass

	for filename in sorted(os.listdir(path)):
		print filename
		tree = etree.parse(path + '/' + filename)
		for elem in tree.iterfind('.//{http://www.w3.org/2005/Atom}entry/{http://www.w3.org/2005/Atom}id'):
			print elem.text
			id = elem.text.split("'")[1]
			for subtree in ['ZaakActoren', 'Statussen', 'KamerstukDossier', 'Documenten', 'Activiteiten', 'Besluiten', 'GerelateerdVanuit', 'GerelateerdNaar', 'HoofdOverig', 'GerelateerdOverig', 'VervangenVanuit', 'VervangenDoor', 'Agendapunten']:
				url = elem.text + '/' + subtree
				resp, content = h.request( url, 'GET' )
				f = open(path+'_'+subtree+'/%s.atom.xml' % (id,), 'w')
				f.write(content)
				f.close()


#try:
#	os.mkdir('DutchRegents/Subtree/Zaken')
#except:
#	pass

str_date = sys.argv[1]
parse_atom('DutchRegents/crawler/%s/GewijzigdOp/Zaken'%(str_date))

