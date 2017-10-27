import sys
from EdgeList import EdgeList


class GraphtoVector:

	
	#list of files location for prov json 
	globalEdgeList = []
	prov_list = []


	def __init__ (self, prov_list):
		#self.globalEdgeList = []

		self.file_list = prov_list    #start from the second element in the list.





	'''This function takes a set of vectors and returns the vector representation'''



	def genVectorSet(self):

		graphVectorSet = []
		edgelist = EdgeList()
		edgelistSet = edgelist.getEdgeListSet(self.file_list) 
		globalEdgeList = edgelist.getUniqueEdgeListSet(edgelistSet)

		# for item in globalEdgeList:
		# 		print(item.toString())



		#passes the edges list of each provenance graph with the global unique set of edges
		for edgeslist in edgelistSet:
			# globalEdgeList_copy = globalEdgeList

			graphVector = self.genVector(globalEdgeList, edgeslist)
			graphVectorSet.append(graphVector)	

			#globalEdgeList_copy = []
		return graphVectorSet





	# def genVector(self, globalEdge, edges):
	
	# 	for edge in edges:
	# 		for i in range(len(globalEdge)):
	# 			if edge == globalEdge[i]:
	# 				globalEdge[i].updateCounter()
	# 				#print(globalEdgeList[i].toString())
	# 		# print("\n")



	# 	#vector = globalEdgeList

	# 	return globalEdge



	''' This function takes a global edge list and an edglist for a graph and
	    returns the vector representation of the edgelist. That is, it counts the number of unique 
	    edges found in the global edge list'''


	def genVector(self, globalEdge, edges):

		vector = [0] * len(globalEdge)

		#print(globalEdge)

	
		for edge in edges:
			for i in range(len(globalEdge)):
				if edge == globalEdge[i]:
					vector[i] += 1

		return vector


	# def addGraphtoVectorSet(self, file):

	# 	edge = EdgeList()

	# 	vectorEdgelist = dge.getEdgeList(file)

	# 	uniqueEdge = uniqueEdgeList(vectorEdgelist)




















