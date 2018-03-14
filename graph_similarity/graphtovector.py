import sys
from EdgeList import EdgeList


class GraphtoVector(object):

    def __init__ (self, prov_list):
        self.file_list = prov_list

    def genVectorSet(self):
        """Converts a set of provenance graph files to a set of vectors.
        """
        graphVectorSet = []
        globalEdgeList = []

        edgelist = EdgeList()
        edgelistSet = edgelist.getEdgeListSet(self.file_list)
        globalEdgeList = edgelist.getUniqueEdgeListSet(edgelistSet)

        for edgeslist in edgelistSet:
            graphVector = self.genVector(globalEdgeList, edgeslist)
            graphVectorSet.append(graphVector)
        return graphVectorSet

    def genVector(self, globalEdge, edges):
        """Converts a single edge set for a graph into a vector.
        
        Constructs a vector by counting the number of times each
        edge in the edges set appears. The globalEdge set defines
        the vector dimensions.
        """
        vector = [0] * len(globalEdge)
        for edge in edges:
            i = globalEdge.index(edge)
            vector[i] += 1
        return vector

