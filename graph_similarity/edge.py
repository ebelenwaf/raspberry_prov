import os

'''
A class for an edge object

'''

class edge:    #class that represents edges
	source_node = ''
	destination_node = ''
	label = ''
	

	def __init__(self, source_node, destination_node, label):
		self.source_node = source_node
		self.destination_node = destination_node
		self.label = label
	def __repr__(self):
		return "Item(%s, %s, %s)" %(self.source_node, self.destination_node, self.label)
	def __eq__(self, other):
		return (self.source_node == other.source_node) and (self.destination_node == other.destination_node) and (self.label == other.label)

	def __hash__(self):
		return hash(self.__repr__())

	#getter functions
	def getDestinationNode():
		return self.destination_node

	def getSourceNode(self):
		return self.source_node

	def getLabel(self):
		return self.source_node

    #setter functions
	def setSourceNode(self, source_node):
		self.source_node = source_node

	def setDestinationNode(self, destination_node):
		self.destination_node = destination_node

	def setLabel(self, label):
		self.label = label


	def isEmpty(self):
		if self.label != NULL or self.source_node != NULL or self.destination_node != NULL:
			return false
		else:
			return true


	def toString(self):
		return 'source node:'+ self.source_node+'\n'+'destination node:'+self.destination_node+'\n'+'\n'+'label:'+self.label

