from lxml import etree
import os
import codecs
import logging
from parlis_settings import settings

logger = logging.getLogger(__name__)

def parse_atom(path, entry, extra = []):
    document_attributen = []
    f = None
    for filename in sorted(os.listdir(path + '_' + entry)):
        print filename
        try:
            tree = etree.parse(path + '_' + entry + '/' + filename)
        except etree.XMLSyntaxError, e:
            logger.exception("XML file %s failed to parse" % (filename, ))
            tree = None
        
        if tree is None:
            continue

        if len(document_attributen) == 0:
            properties = tree.find('.//{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties')
            if properties is not None:
                document_attributen = [x.tag.split('}')[1] for x in properties.getchildren()]
                f = codecs.open('Zaken_' + entry + '.tsv', 'w', 'UTF-8')
                f.write('\t'.join(document_attributen + extra) + '\n')

        SID = tree.find('.//{http://www.w3.org/2005/Atom}id')
        if SID is None:
            continue

        SID = SID.text.split('\'')[1]

        for subtree in tree.iterfind('.//{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
            row = []
            for x in document_attributen:
                attribuut = subtree.find('.//{http://schemas.microsoft.com/ado/2007/08/dataservices}'+x)
                if attribuut is not None and attribuut.text is not None:
                    row.append(attribuut.text.replace('\n', ' ').replace('\t', ' ').replace('\r',''))
                else:
                    row.append('')
            row.append(SID)
            f.write('\t'.join(row) + '\n')
    if f is not None:
        f.flush()
        f.close()

def parse_zaken(root):
    for subtree in ['Activiteiten','Agendapunten','Besluiten','Documenten','GerelateerdNaar','GerelateerdOverig','GerelateerdVanuit','HoofdOverig','KamerstukDossier','Statussen','VervangenDoor','VervangenVanuit','ZaakActoren']:
        parse_atom(root, subtree, ['SID_Zaak'])

