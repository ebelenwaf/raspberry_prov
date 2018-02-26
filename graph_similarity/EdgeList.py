import json
from edge import edge
from pprint import pprint

class EdgeList:

	prov_json = ''


	'''
	   This function converts a provenance graph (json object file)
	   into an edge list. An edge consists of source, destionation 
	   node and a counter.
	'''
	    
	def getEdgeList(self, prov_json_file):

		edgeJsonList = []
		edgeLabel = []
		loopCounter = 0
		edgeList = []

		
		json_data = open(prov_json_file).read()
		provJsonData = json.loads(json_data)
		




		#finds edge labes with names wasAssociatedWith,
		#wasGeneratedBy, and used...


		#edge_label = ['wasAssociatedWith', 'wasGeneratedBy', 'used']
		edge_label = ['wasAssociatedWith', 'wasGeneratedBy', 'actedOnBehalfOf', 'wasDerivedFrom']

		# edgeJsonList.append(provJsonData['wasAssociatedWith'])
		# edgeJsonList.append(provJsonData['wasGeneratedBy'])
		# edgeJsonList.append(provJsonData['used'])


		for label in edge_label:
			if label in provJsonData:
				edgeJsonList.append(provJsonData[label])


		#list of edge label values
		# edgeLabel.append('wasAssociatedWith')
		# edgeLabel.append('wasGeneratedBy')
		# edgeLabel.append('used')

		edgeLabel.append('wasAssociatedWith')
		edgeLabel.append('wasGeneratedBy')
		edgeLabel.append('actedOnBehalfOf')
		edgeLabel.append('wasDerivedFrom')


		#print(edgeLabel)

		








		#creates an edge object with the source and destionation nodes 
		#from the prov json graph and stores the edge object in a list.
		for i in range(len(edgeJsonList)):
			for data, value in edgeJsonList[i].items():
				key_list = list(value.keys())
				destination_node = value[key_list[0]]
				source_node = value[key_list[1]]

				# if 'entity' in key_list[1]:
				if 'event' in source_node:
					source_node = str(provJsonData['entity'][source_node])
					#print("Source Node"+source_node)
				# elif 'activity' in source_node:
				# 	source_node = value[key_list[1]]   #FIXME: change to prov:type value
				# elif 'agent' in source_node:
				# 	source_node = str(provJsonData['activity'][source_node]['prov:type'])


				# elif 'entity' in key_list[0]:
				elif 'event' in destination_node:
					destination_node = str(provJsonData['entity'][destination_node])
					# print("\n Destination Node:"+destination_node)
				# else:
				# 	source_node = value[key_list[0]]
				# 	print(source_node)





				#creates edge objects
				edgeVal = edge(source_node, destination_node, edgeLabel[i])

				#print(edgeVal.toString())

				#adds edge to a list
				#print(loopCounter)
				edgeList.append(edgeVal)
		#loopCounter += 1

		return edgeList



	def getCounterList(edgelist):
		edges = []
		for edge in edgeList:
			edges.append(edge.getCounter())

		return edges



	def getUniqueEdgeList(self, edgelist):
		# fileList = EdgeList()
		# edgelist = self.getEdgeList(file_location)
		s = set()
		for item in edgelist:
			s.add(item)

		return list(s)

	def getUniqueEdgeListSet(self, edgelistSet):
		s = set() 
		for edgelist in edgelistSet:
			for item in edgelist:
				s.add(item)
		# for item in list(s):
		# 	print(item)

		return list(s)

	def getEdgeListSet(self, file_location_list):
		edgelistFinal = []
		for file in file_location_list:
			#edges = EdgeList()
			edgelist = self.getEdgeList(file)
			edgelistFinal.append(edgelist)
			#print(edgelist)
		return edgelistFinal

# vector = EdgeList()

# edges = vector.getEdgeList("output.json")
# vectorList = vector.getUniqueEdgeList(edges)

# # edgelist = vector.getEdgeList("output.json")
# # print(vectorList)

# # print("\n")

# # print(edgelist)

# file_list = ['output.json', 'output.json']

# edgelistSet = vector.getEdgeListSet(file_list)

# d = vector.getUniqueEdgeListSet(edgelistSet)

# print(edgelistSet)

# print("\n")

# print(d)









		





