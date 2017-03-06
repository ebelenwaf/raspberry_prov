#!/usr/bin/env
import sys
import re
#... rest of code
# visualize the graph
from prov.dot import prov_to_dot
from prov.model import ProvDocument
d1 = ProvDocument()  # d1 is now an empty provenance document
c = 0
def main():
	with open('../ctf-output.txt', 'r') as file_object:
		readFile(file_object)

	d1.serialize(indent=2)
	d1.serialize('article-prov.json')
	dot = prov_to_dot(d1)
	dot.write_png('article-prov.png')



def readFile(file):
	d1.add_namespace('senread', 'www.google.com')
	for line in file:
		ctfToProv(d1, line)
	
	#print d1.get_provn()
	#d1.entity('ex', [ prov:type='SensorReading'])
	#d1.activity('ex', timestamp, , [SenRead:temperature=])
	




def ctfToProv(prov_dm, line):
	global c
	# Create a new provenance document
	m = re.compile(r"\{(.*?)\}")
	timestamp = line[line.find('[') + 1: line.find(']')]
	#print timestamp
	''' Gets the attributes for the sensor readings'''
	attribute= m.search(line, line.find(',')).group(1).split(',') 
	dictionary = seperateField(attribute)
	tags = ['prov:Temperature', 'prov:Humidity', 'prov:OtherReadings', 'prov:State']
	prov_dm.agent(tags[0])
	attributes = {tags[x]: attribute[x][attribute[x].find('=')+1:] for x in range(1, len(tags))}
	attributes['prov:TimeStamp'] = timestamp
	l = ['senread:me', 'senread:you', 'senread:us', 'senread:who']
	e1 = prov_dm.entity(l[c], attributes)
	c = (c+1)% len(l)
	prov_dm.wasAttributedTo(e1, tags[c])
	#prov_dm.entity(attributes)
	# Agent: nowpeople:Bob
	'''
	d1.agent('Bob')
	# Attributing the article to the agent
	d1.wasAttributedTo(e1, 'nowpeople:Bob')
	# What we have so far (in PROV-N)
	
	# 'now:employment-article-v1.html' was derived from govftp
	d1.add_namespace('govftp', 'ftp://ftp.bls.gov/pub/special.requests/oes/')
	d1.add_namespace('void', 'http://vocab.deri.ie/void#')
	d1.entity('govftp:oesm11st.zip', {'prov:label': 'employment-stats-2011', 'prov:type': 'void:Dataset'})
	d1.wasDerivedFrom('now:employment-article-v1.html', 'govftp:oesm11st.zip')

	#print d1.get_provn()

	# Adding an activity
	d1.add_namespace('is', 'http://www.provbook.org/nownews/is/#')
	d1.activity('is:writeArticle')

	# Usage and Generation
	d1.used('is:writeArticle', 'govftp:oesm11st.zip')
	d1.wasGeneratedBy('now:employment-article-v1.html', 'nowpeople:Bob')
	#Prints to console
	# print d1.serialize(indent=2)  d1.serialize('article-prov.json')
'''
	# Install pydotplus and graphwiz if you want to see graph

	'''
	'''
	#d2 = ProvDocument.deserialize('article-prov.json')

''' Seperates an entry in a list into a key and value pair in a dictionary.
Example entry will look like ['Temperature = -1'], output would be {'Temperature': -1}
'''
def seperateField(a):
	return {x[:x.find("=")]: x[x.find("=")+1:] for x in a}	
main()
