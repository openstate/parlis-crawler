from lxml import etree
import os
import codecs

root = '/mnt/tmp/apicrawl/DutchRegents/GewijzigdOp'

def parse_atom(path, entry, attributes,  extra = []):
	f = codecs.open(entry + '.tsv', 'w', 'UTF-8')
	f.write('\t'.join(attributes + extra) + '\n')
	for filename in sorted(os.listdir(path + '/' + entry)):
		print filename
		tree = etree.parse(path + '/' + entry + '/' + filename)

		for elem in tree.iterfind('.//{http://www.w3.org/2005/Atom}entry'):
			subtree = elem.find('.//{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties')
			row = []
			for x in document_attributen:
				attribuut = subtree.find('.//{http://schemas.microsoft.com/ado/2007/08/dataservices}'+x)
				if attribuut is not None and attribuut.text is not None:
					row.append(attribuut.text.replace('\n', ' ').replace('\t', ' ').replace('\r', ''))
				else:
					row.append('')
			f.write('\t'.join(row) + '\n')
	f.close()

document_attributen = ['Id', 'Nummer', 'Soort', 'Titel', 'CiteerTitel', 'Alias', 'Status', 'Onderwerp', 'DatumStart', 'Kamer', 'GrondslagVoorhang', 'Termijn', 'Vergaderjaar', 'Volgnummer', 'HuidigeBehandelStatus', 'Afgedaan', 'GrootProject', 'AangemaaktOp', 'GewijzigdOp']

parse_atom(root, 'Zaken', document_attributen, [])

