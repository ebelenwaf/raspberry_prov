#!/usr/bin/env
import babeltrace
import sys
import re
from prov.dot import prov_to_dot
from prov.model import ProvDocument


# get the trace path from the first command line argument
trace_path = sys.argv[1]

trace_collection = babeltrace.TraceCollection()

trace_collection.add_trace(trace_path, 'ctf')
#Outputs the event keys of each trace that was recorded.
def ctfToProv():
    d1 = ProvDocument()
    ex = Namespace('ex', 'http://example/')  # namespaces do not need to be explicitly added to a document
#   results = open('output.txt', 'w')
    agents = ['SensorOne', 'SensorTwo', 'SensorThree']
    data = ['timestamp', 'humidity', 'temperature']
    for event in trace_collection.events:

        for data in event.keys():

            print(('%s : %s ,' %(key, event[key])))
#           results.write(('%s : %s ,' %(key, event[key])))
        print('\n')
#	with open('../ctf-output.txt', 'r') as file_object:
#		readFile(file_object)
#
#	d1.serialize(indent=2)
#	d1.serialize('article-prov.json')
#	dot = prov_to_dot(d1)
#	dot.write_png('article-prov.png')
#
#	attributes['prov:TimeStamp'] = timestamp
#	l = ['senread:me', 'senread:you', 'senread:us', 'senread:who']
#	e1 = prov_dm.entity(l[c], attributes)
#	c = (c+1)% len(l)
#	prov_dm.wasAttributedTo(e1, tags[c])
#	#prov_dm.entity(attributes)
ctfToProv()
