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

            for subtree in ['ActiviteitActoren', 'Agendapunten', 'Documenten', 'Zaken', 'VoortgezetVanuit', 'VoortgezetIn', 'VervangenVanuit', 'VervangenDoor', 'Reserveringen']:
                subtree_file_name = path+'_'+subtree+'/%s.atom.xml' % (id,)
                if not os.path.exists(subtree_file_name):
                    url = elem.text + '/' + subtree
                    resp, content = h.request( url, 'GET' )
                    f = open(subtree_file_name, 'w')
                    f.write(content)
                    f.close()

# parse_atom('DutchRegents/Activiteiten')

