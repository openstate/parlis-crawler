import os
import codecs
import shutil

root = '/mnt/tmp/apicrawl/output/Bestanden/'
txt = '/mnt/tmp/apicrawl/output/txt/'

f = codecs.open('Documenten.tsv')

for row in f.read().split('\n'):
	attributes = row.split('\t')
	dst = txt + attributes[0] + '.txt'

	if not os.path.exists(dst):
		src = root + attributes[0]

		if attributes[17] == 'text/plain':
			shutil.copyfile(src, dst)
		elif attributes[17] == 'application/pdf':
			os.system("/usr/bin/pdftotext -layout %s %s" % (src, dst))
		elif attributes[17] == 'application/msword':
			os.system("/usr/bin/wvText %s %s" % (src, dst))
		elif attributes[17] == 'text/richtext':
			os.system("/usr/bin/catdoc %s 1>%s" % (src, dst))
		elif attributes[17] == 'text/html':
			os.system("/usr/bin/elinks -dump %s 1>%s" % (src, dst))
		elif attributes[17] == 'application/octet-stream' or attributes[17] == 'application/xml':
			os.system("/usr/bin/docx2txt %s %s" % (src, dst))
		else:
			print attributes[0], attributes[17]
		
	
