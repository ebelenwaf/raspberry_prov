#!/usr/bin/env
import babeltrace
import sys
import re
from prov.dot import prov_to_dot
from prov.model import ProvDocument, Namespace, Literal, PROV, Identifier


# get the trace path from the first command line argument
trace_path = sys.argv[1]
trace_collection = babeltrace.TraceCollection()
trace_collection.add_trace(trace_path, 'ctf')
#Outputs the event keys of each trace that was recorded.
def ctfToProv():
    d1 = ProvDocument()
    ex = Namespace('ex', 'http://example/')  # namespaces do not need to be explicitly added to a document
    data = ['timestamp', 'humidity', 'temperature', 'sensor_info', 'device_info']
    for event in trace_collection.events:

        dataset = {'ex:'+data[0]:event[data[0]], 'ex:'+data[1]:event[data[1]], 'ex:'+data[2]:event[data[2]]}
        e1 = d1.entity(ex['dataset'],dataset)
        sensor_agent = d1.agent('ex:'+event['sensor_info'])
        device_agent = d1.agent('ex:'+event['device_info'])
        activity = d1.activity('ex:read')
        d1.wasGeneratedBy(e1, activity)
        d1.wasAssociatedWith(activity,sensor_agent)
        d1.used(sensor_agent, device_agent)
        d1.serialize('hey.json')
    return d1
prov_document = ctfToProv()
