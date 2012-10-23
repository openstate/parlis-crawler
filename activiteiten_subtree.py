from lxml import etree
import os
import codecs
import httplib2

h = httplib2.Http(disable_ssl_certificate_validation=True)
h.add_credentials( 'SOS', 'Open2012' )

def parse_atom(path):
	for filename in sorted(os.listdir(path)):
		print filename
		tree = etree.parse(path + '/' + filename)
		for elem in tree.iterfind('.//{http://www.w3.org/2005/Atom}entry/{http://www.w3.org/2005/Atom}id'):
			print elem.text
			id = elem.text.split("'")[1]

			for subtree in ['ActiviteitActoren', 'Agendapunten', 'Documenten', 'Zaken', 'VoortgezetVanuit', 'VoortgezetIn', 'VervangenVanuit', 'VervangenDoor', 'Reserveringen']:
				url = elem.text + '/' + subtree
				resp, content = h.request( url, 'GET' )
				f = open('DutchRegents/'+subtree+'/%s.atom.xml' % (id,), 'w')
				f.write(content)
				f.close()

parse_atom('DutchRegents/Activiteiten')

