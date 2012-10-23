from lxml import etree
import sys
import os
import codecs
import httplib2
import datetime

h = httplib2.Http(disable_ssl_certificate_validation=True)
h.add_credentials( 'SOS', 'Open2012' )

def parse_atom(path, skipuntil):
	for subtree in ['ZaakActoren', 'Statussen', 'KamerstukDossier', 'Documenten', 'Activiteiten', 'Besluiten', 'GerelateerdVanuit', 'GerelateerdNaar', 'HoofdOverig', 'GerelateerdOverig', 'VervangenVanuit', 'VervangenDoor', 'Agendapunten']:
		try:
			os.mkdir(path+'_'+subtree)
		except:
			pass

	skip = True
	for filename in sorted(os.listdir(path)):
		if skip and not filename.startswith(skipuntil):
			continue
		else:
			skip = False

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


parse_atom('DutchRegents/crawler/%s/GewijzigdOp/Zaken'%(datetime.date.today()), sys.argv[1])
