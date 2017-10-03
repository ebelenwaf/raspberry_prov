#!/usr/bin/env python

import yaml

def event_field(config_file):

	with open(config_file, 'r') as stream:
	    try:
	        list_doc = yaml.load(stream)

	        value = list_doc["metadata"]

	        val = value['streams']

	        default = val['default']

	        events = default['events']
	        sensor_events = events['sensor_events']


	        payload_type = sensor_events['payload-type']

	        fields = payload_type['fields']

	        event_value = fields.keys()


	        #for event in event_value:
	        	#print(event)

	    except yaml.YAMLError as exc:
	        print(exc)

	return list(event_value)
