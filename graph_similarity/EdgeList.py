import json

from edge import edge
from pprint import pprint

class EdgeList(object):

    def getEdgeList(self, prov_json_file):
        """Converts a provenance graph file into an edge list.
        
        Creates a list of labeled, directed edges.
        """
        edgeJsonList = []
        edgeLabel = []
        loopCounter = 0
        edgeList = []
        json_data = None
        
        with open(prov_json_file) as json_file:
            json_data = json_file.read()
        provJsonData = json.loads(json_data)

        # For edge labels given (wAW, wGB, u), create an edge object with
        # the source and destination nodes from the prov json graph and
        # store the edges in a list.
        edge_label = ['wasAssociatedWith', 'wasGeneratedBy', 'used']
        for label in edge_label:
            for data, value in provJsonData[label].items():
                keys = value.keys()
                destination_node = value[keys[0]]
                source_node = value[keys[1]]
                edgeVal = edge(source_node, destination_node, label)
                edgeList.append(edgeVal)
        return edgeList

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

