from prov.model import ProvDocument, Namespace, Literal, PROV, Identifier



class entityActivity:



	# def __init__(self, entity, activity):
	# 	self.entity = entity
	# 	self.activity = activity


	def getEntity(self):
		return self.entity

	def getActivity(self):
		return self.activity

	def addData(self, entity, activity):
		self.entity = entity
		self.activity = activity


