from prov.dot import prov_to_dot
from provneo4j.api import Api
import provneo4j.tests.examples as examples
from prov.model import ProvDocument, Namespace, Literal, PROV, Identifier
import datetime

provneo4j_api = Api(base_url="http://localhost:7474/db/data", username="neo4j", password="database")

def primer():
	a  = ProvDocument()
	with open("/Users/andrecampbell/Google Drive/Sophomore Year/Research/raspberry_prov/babelt_work/output.json") as json_file:
		line = json_file.readline()
		print line
		a.deserialize(content=line)
	print a.get_provn()
	return a


prov_document = primer()

# Store the document to ProvStore:
#   - the public parameter is optional and defaults to False
provneo4j_api.document.create(prov_document, name="Primer Example")

# => This will store the document and return a ProvStore Document object
