#!/usr/bin/env python

import sys
import os
import codecs
import httplib2
import datetime
import logging
from lxml import etree

from parlis_utils import get_http_client

h = get_http_client()

logger = logging.getLogger(__name__)

def parse_atom(path):
	for subtree in ['ZaakActoren', 'Statussen', 'KamerstukDossier', 'Documenten', 'Activiteiten', 'Besluiten', 'GerelateerdVanuit', 'GerelateerdNaar', 'HoofdOverig', 'GerelateerdOverig', 'VervangenVanuit', 'VervangenDoor', 'Agendapunten']:
		try:
			os.mkdir(path+'_'+subtree)
		except:
			pass

	for filename in sorted(os.listdir(path)):
		logger.info(filename)
		tree = etree.parse(path + '/' + filename)
		for elem in tree.iterfind('.//{http://www.w3.org/2005/Atom}entry/{http://www.w3.org/2005/Atom}id'):
			logger.info(elem.text)
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

if __name__ == '__main__':
    from_date = sys.argv[1]
    till_date = sys.argv[2]
    parse_atom('DutchRegents/crawler/%s/GewijzigdOp/Zaken'%(str_date))

