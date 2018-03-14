import json

from edge import edge
from pprint import pprint

class EdgeList:

    prov_json = ''

    def getEdgeList(self, prov_json_file):
        """Converts a provenance graph file into an edge list.
        
        Creates a list of edges, where an edge consists of source, destination
        node and a counter.
        """
        edgeJsonList = []
        edgeLabel = []
        loopCounter = 0
        edgeList = []

        json_data = open(prov_json_file).read()
        provJsonData = json.loads(json_data)

        #finds edge labes with names wasAssociatedWith,
        #wasGeneratedBy, and used...
        edge_label = ['wasAssociatedWith', 'wasGeneratedBy', 'used']
        for label in edge_label:
            if label in provJsonData:
                edgeJsonList.append(provJsonData[label])

        #list of edge label values
        edgeLabel.append('wasAssociatedWith')
        edgeLabel.append('wasGeneratedBy')
        edgeLabel.append('used')

        #creates an edge object with the source and destionation nodes
        #from the prov json graph and stores the edge object in a list.
        for i in range(len(edgeJsonList)):
            for data, value in edgeJsonList[i].items():
                key_list = list(value.keys())
                destination_node = value[key_list[0]]
                source_node = value[key_list[1]]

                edgeVal = edge(source_node, destination_node, edgeLabel[i])
                edgeList.append(edgeVal)
        return edgeList

    def getCounterList(edgelist):
        edges = []
        for edge in edgeList:
            edges.append(edge.getCounter())
        return edges

    def getUniqueEdgeList(self, edgelist):
        s = set()
        for item in edgelist:
            s.add(item)
        return list(s)

    def getUniqueEdgeListSet(self, edgelistSet):
        s = set()
        for edgelist in edgelistSet:
            for item in edgelist:
                s.add(item)
        return list(s)

    def getEdgeListSet(self, file_location_list):
        edgelistFinal = []
        for file in file_location_list:
            edgelist = self.getEdgeList(file)
            edgelistFinal.append(edgelist)
        return edgelistFinal

