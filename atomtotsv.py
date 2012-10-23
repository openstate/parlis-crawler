from lxml import etree
import os
import codecs

root = '/mnt/tmp/apicrawl/output'

def parse_atom(path, entry, attributes,  extra = []):
	f = codecs.open(entry + '.tsv', 'w', 'UTF-8')
	f.write('\t'.join(attributes + extra) + '\n')
	for filename in sorted(os.listdir(path + '/' + entry)):
		print filename
		tree = etree.parse(path + '/' + entry + '/' + filename)
		
		for elem in tree.iterfind('.//{http://www.w3.org/2005/Atom}entry'):
			content_type = elem.find('.//{http://www.w3.org/2005/Atom}content').attrib["type"]
			if content_type == '':
				print etree.tostring(elem)
			subtree = elem.find('.//{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties')
			row = []
			for x in document_attributen:
				attribuut = subtree.find('.//{http://schemas.microsoft.com/ado/2007/08/dataservices}'+x)
				if attribuut is not None and attribuut.text is not None:
					row.append(attribuut.text.replace('\n', ' ').replace('\t', ' '))
				else:
					row.append('')
			row.append(content_type)
			f.write('\t'.join(row) + '\n')
	f.close()

document_attributen = ['Id', 'DocumentNummer', 'Titel', 'Soort', 'Onderwerp', 'Datum', 'Volgnummer', 'Vergaderjaar', 'Kamer', 'AangemaaktOp', 'GewijzigdOp', 'Citeertitel', 'Alias', 'DatumRegistratie', 'DatumOntvangst', 'AanhangelNummer', 'KenmerkAfzender']
parse_atom(root, 'Documenten', document_attributen, ['ContentType'])

