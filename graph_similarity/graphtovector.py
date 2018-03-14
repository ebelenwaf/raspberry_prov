import sys
from EdgeList import EdgeList


class GraphtoVector:

    #list of files location for prov json
    globalEdgeList = []
    prov_list = []

    def __init__ (self, prov_list):
        self.file_list = prov_list

    def genVectorSet(self):
        '''This function takes a set of vectors and returns the vector representation'''

        graphVectorSet = []
        edgelist = EdgeList()
        edgelistSet = edgelist.getEdgeListSet(self.file_list)
        globalEdgeList = edgelist.getUniqueEdgeListSet(edgelistSet)

        #passes the edges list of each provenance graph with the global unique set of edges
        for edgeslist in edgelistSet:
            graphVector = self.genVector(globalEdgeList, edgeslist)
            graphVectorSet.append(graphVector)
        return graphVectorSet

    def genVector(self, globalEdge, edges):
    ''' This function takes a global edge list and an edglist for a graph and
        returns the vector representation of the edgelist. That is, it counts the number of unique
        edges found in the global edge list'''

        vector = [0] * len(globalEdge)

        for edge in edges:
            for i in range(len(globalEdge)):
                if edge == globalEdge[i]:
                    vector[i] += 1

        return vector

