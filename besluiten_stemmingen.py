from lxml import etree
import os
import codecs
import httplib2

from parlis_utils import get_http_client

h = get_http_client()

def parse_atom(path):
	for filename in sorted(os.listdir(path)):
		print filename
		tree = etree.parse(path + '/' + filename)
		for elem in tree.iterfind('.//{http://www.w3.org/2005/Atom}entry/{http://www.w3.org/2005/Atom}id'):
			print elem.text
			id = elem.text.split("'")[1]
			url = elem.text + '/Stemmingen'
			resp, content = h.request( url, 'GET' )
			f = open('DutchRegents/Stemmingen/%s.atom.xml' % (id,), 'w')
			f.write(content)
			f.close()

# parse_atom('DutchRegents/Besluiten')

