#!/usr/bin/env
#import provneo4j.api
#from yaml_1 import event_field
import babeltrace
import sys
import os
import datetime
from prov.dot import prov_to_dot
from prov.model import ProvDocument, Namespace, Literal, PROV, Identifier
#import yaml

#provneo4j_api = provneo4j.api.Api(base_url="http://localhost:7474/db/data", username="neo4j", password="neo4j")

# get the trace path from the first command line argument
trace_path = sys.argv[1]
trace_collection = babeltrace.TraceCollection()
trace_handle = trace_collection.add_trace(trace_path,'ctf')
if trace_handle is None:
    raise RuntimeError('Cannot add trace')

#Outputs the event keys of each trace that was recorded.
def ctfToProv():
    d1 = ProvDocument()
    dummy = ProvDocument()
    ex = Namespace('ex', 'http://example/')  # namespaces do not need to be explicitly added to a document
    #data = event_field(os.path.join(trace_path,'../config.yaml'))
    counter = 0
    counter_1 = 0
    relationships = []
    entities = []
    activities = []
    for event in trace_collection.events:
        dataset = {'ex:'+k:event[k] for k in event.field_list_with_scope(
            babeltrace.CTFScope.EVENT_FIELDS)}
        dataset.update({'ex:'+'timestamp':(event['timestamp']/1000000000)})
        #dataset.update({'ex:'+'name':event.name})

        e1 = d1.entity(ex['event'+str(counter)],dataset)
        entities.append(e1)
        producer_agent = d1.agent('ex:'+event['producer_id'])
        controller_agent = d1.agent('ex:'+event['controller_id'])
        activity = d1.activity('ex:'+event['activity']+str(counter_1))
        activities.append(activity)
        #d1.wasGeneratedBy(e1, activity)
        # strings used to detect if the relationship already exists in the d1 document
        association_relationship = str(dummy.wasAssociatedWith(activity, producer_agent))
        used_relationship = str(dummy.used(controller_agent, producer_agent))

        #add activity to producer agent
       # d1.wasAssociatedWith(activity,producer_agent)
        #check if the association already esists
        # if association_relationship not in relationships:
        #     d1.wasAssociatedWith(activity,producer_agent)
        #     relationships.append(association_relationship)
        if used_relationship not in relationships:
            d1.used(controller_agent, producer_agent)
            relationships.append(used_relationship)
        counter+=1
        counter_1 +=1
    for index in range(len(entities)-1):
        d1.wasAssociatedWith(entities[index], entities[index + 1])

    for index in range(len(entities)):
        d1.wasGeneratedBy(entities[index], activities[index])
        d1.wasAssociatedWith(activities[index],producer_agent)

    return d1
prov_document = ctfToProv()
prov_document = prov_document.unified()
prov_document.serialize('output.json')
#prov_document.serialize('output.json')
#provneo4j_api.document.create(prov_document, name="Primer Example")





