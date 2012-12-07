from lxml import etree
import os
import codecs

def parse_atom(path, entry, extra = []):
	document_attributen = []
	f = None
	for filename in sorted(os.listdir(path + '/' + entry)):
		print filename
		tree = etree.parse(path + '_' + entry + '/' + filename)

		if len(document_attributen) == 0:
			properties = tree.find('.//{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties')
			if properties is not None:
				document_attributen = [x.tag.split('}')[1] for x in properties.getchildren()]
				f = codecs.open('Activiteiten_' + entry + '.tsv', 'w', 'UTF-8')
				f.write('\t'.join(document_attributen + extra) + '\n')

		SID = tree.find('.//{http://www.w3.org/2005/Atom}id').text.split('\'')[1]

		for elem in tree.iterfind('.//{http://www.w3.org/2005/Atom}entry'):
			subtree = elem.find('.//{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties')
			row = []
			for x in document_attributen:
				attribuut = subtree.find('.//{http://schemas.microsoft.com/ado/2007/08/dataservices}'+x)
				if attribuut is not None and attribuut.text is not None:
					row.append(attribuut.text.replace('\n', ' ').replace('\t', ' ').replace('\r',''))
				else:
					row.append('')
			row.append(SID)
			f.write('\t'.join(row) + '\n')
	f.close()

def parse_activiteiten(root):
    for subtree in ['ActiviteitActoren', 'Agendapunten', 'Documenten', 'Zaken', 'VoortgezetVanuit', 'VoortgezetIn', 'VervangenVanuit', 'VervangenDoor', 'Reserveringen']:
    	parse_atom(root, subtree, ['SID_Activiteit'])

