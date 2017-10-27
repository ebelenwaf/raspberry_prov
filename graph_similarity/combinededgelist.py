from EdgeList import EdgeList

class CombinedEdgeList:

	"""
		This function takes a list of prov json file 
		and returns a list of edgelist objects. This information is used to 
		combine the total unique edges (global edge list) of all the graphs in the set.

	"""

	file_location_list = ""


	def __init__ (self, file_location_list):
		self.file_location_list = file_location_list

	# def graphsetEdgeList(self):
	# 	edgelist = []
	# 	edgelistFinal = []
	# 	for file in self.file_location_list:
	# 		edges = EdgeList()

	# 		edgelist = edges.getEdgeList(file)

	# 		edgelistFinal.append(edgelist)

	# 	return edgelistFinal


	# ''' This function takes a list of edgelist objects and returns a combination  of unique edges.
	#     This forms the dimensionality of the set of edges.
 #    '''

	# def uniqueEdgeListSet(self, edgelistFinal):
	# 	firstEdgeList = []
	# 	if len(edgelistFinal)!=0:
	# 		firstEdgeList = self.uniqueEdgeList(edgelistFinal[0])
	# 	for i in range(len(edgelistFinal)):
	# 		for edge in edgelistFinal[i]:
	# 			print(edge)
	# 			for j in range(len(firstEdgeList)):
	# 				if edge == firstEdgeList[j]: #found identical edge, exit
	# 					break 
	# 			#reached the end of the list, add edge to the list
	# 			print("loop was here! append")
	# 			firstEdgeList.append(edge)
	# 		continue

	# 	return firstEdgeList


	# def uniqueEdgeList(self, edgeList):
	# 	for i in range(len(edgeList)):
	# 		for j in range(len(edgelist)):
	# 			if edgelist[i] == edgeList[j+1]:
	# 				del edgeList[j]
	# 	return edgeList

	def uniqueEdgeList(self):

		fileList = EdgeList()

		edgelist = fileList.getEdgeList(self.file_location_list)


		s = set()
		for item in edgelist:
			s.add(item)
		edgelist = list(s)
		
		return edgelist




comb = CombinedEdgeList("output.json")



list_x  = comb.uniqueEdgeList()


for list_y in list_x:
	print(list_y.toString())












		














	

