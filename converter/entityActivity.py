from prov.model import ProvDocument, Namespace, Literal, PROV, Identifier



class entityActivity:



	def __init__(self):
		self.entity = None
		self.activity = None


	def getEntity(self):
		return self.entity

	def getActivity(self):
		return self.activity

	def addData(self, entity, activity):
		self.entity = entity
		self.activity = activity


