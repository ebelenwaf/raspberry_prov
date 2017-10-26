from prov.dot import prov_to_dot
from provneo4j.api import Api
import provneo4j.tests.examples as examples
from prov.model import ProvDocument, Namespace, Literal, PROV, Identifier
import datetime
import os

provneo4j_api = Api(base_url="http://localhost:7474/db/data", username="neo4j", password="database")


# Function reads the output.json file to gather the serialized Prov Document, deserializes it and returns the Prov Document. 
def primer():
        a  = ProvDocument()
        script_path = os.path.dirname(os.path.abspath( __file__ )) #
        with open(str(script_path) + "/output.json") as json_file:
                line = json_file.readline()
                a =  a.deserialize(content=line)
        return a


prov_document = primer()

# Store the document to ProvStore:
#   - the public parameter is optional and defaults to False
provneo4j_api.document.create(prov_document, name="Primer Example")

# => This will store the document and return a ProvStore Document object

dot = prov_to_dot(prov_document)
#dot.write_png('article-prov.png')
dot.write_pdf('article-prov.pdf')
