from lxml import etree
import os
import codecs
import httplib2

from parlis_utils import get_http_client

h = get_http_client()

def parse_atom(path):
    try:
        os.mkdir(path+'_Stemmingen')
    except:
        pass
    
	for filename in sorted(os.listdir(path)):
		print filename
		tree = etree.parse(path + '/' + filename)
		for elem in tree.iterfind('.//{http://www.w3.org/2005/Atom}entry/{http://www.w3.org/2005/Atom}id'):
			print elem.text
			id = elem.text.split("'")[1]
			url = elem.text + '/Stemmingen'
			resp, content = h.request( url, 'GET' )
			file_name = path + '_Stemmingen/%s.atom.xml' % (id,)
			f = open(file_name, 'w')
			f.write(content)
			f.close()

# parse_atom('DutchRegents/Besluiten')

