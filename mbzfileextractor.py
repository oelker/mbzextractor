import xml.etree.ElementTree as etree
import fnmatch
import shutil
import os
import re

#change the mbz to .zip and unpack it first, put all the contents you unpack in the source directory you then point to below.

def locate(pattern, root=os.curdir):
    '''Locate all files matching supplied filename pattern in and below
    supplied root directory.'''
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)

destination = '/Users/soelker/mbzfileextractor/moodlebackupdestination/'
source      = '/Users/soelker/mbzfileextractor/moodlebackupsource/'
pattern     = re.compile('^\s*(.+\.(?:pdf|jpg|ppt|doc|png|zip|rtf|sav|mp3|mht|por|xlsx?|docx?|pptx?))\s*$', flags=re.IGNORECASE)

tree = etree.parse(source + 'files.xml')
root = tree.getroot()

print( "Root: ", root)

for rsrc in root:
	#print ("Child id: ", rsrc.attrib)
	fhash = rsrc.find('contenthash').text
	fname = rsrc.find('filename').text

	#print ("\tHash: '", fhash, "'")
	#print ("\tName: '", fname, "'")

	hit = pattern.search(fname)

	if hit:
		#print ("\tMatch: ", hit.group(1))
		files = locate(fhash, source)
		#print ("\tFiles: ", files)
		for x in files:
			print ("Copying: ", x)
			shutil.copyfile(x, destination + fname)
	else: 
		print ("No Match: '", fname, "'")
