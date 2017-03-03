from provneo4j.api import Api
import provneo4j.tests.examples as examples
from prov.model import ProvDocument, Namespace, Literal, PROV, Identifier
import datetime

provneo4j_api = Api(base_url="http://localhost:7474/db/data", username="neo4j", password="database")

def primer_example():
    # https://github.com/lucmoreau/ProvToolbox/blob/master/prov-n/src/test/resources/prov/primer.pn
    #===========================================================================
    # document
    g = ProvDocument()

    #    prefix ex <http://example/>
    #    prefix dcterms <http://purl.org/dc/terms/>
    #    prefix foaf <http://xmlns.com/foaf/0.1/>
    ex = Namespace('ex', 'http://example/')  # namespaces do not need to be explicitly added to a document
    g.add_namespace("dcterms", "http://purl.org/dc/terms/")
    g.add_namespace("foaf", "http://xmlns.com/foaf/0.1/")

    #    entity(ex:article, [dcterms:title="Crime rises in cities"])
    # first time the ex namespace was used, it is added to the document automatically
    g.entity(ex['article'], {'dcterms:title': "Crime rises in cities"})
    #    entity(ex:articleV1)
    g.entity(ex['articleV1'])
    #    entity(ex:articleV2)
    g.entity(ex['articleV2'])
    #    entity(ex:dataSet1)
    g.entity(ex['dataSet1'])
    #    entity(ex:dataSet2)
    g.entity(ex['dataSet2'])
    #    entity(ex:regionList)
    g.entity(ex['regionList'])
    #    entity(ex:composition)
    g.entity(ex['composition'])
    #    entity(ex:chart1)
    g.entity(ex['chart1'])
    #    entity(ex:chart2)
    g.entity(ex['chart2'])
    #    entity(ex:blogEntry)
    g.entity(ex['blogEntry'])

    #    activity(ex:compile)
    g.activity('ex:compile')  # since ex is registered, it can be used like this
    #    activity(ex:compile2)
    g.activity('ex:compile2')
    #    activity(ex:compose)
    g.activity('ex:compose')
    #    activity(ex:correct, 2012-03-31T09:21:00, 2012-04-01T15:21:00)
    g.activity('ex:correct', '2012-03-31T09:21:00', '2012-04-01T15:21:00')  # date time can be provided as strings
    #    activity(ex:illustrate)
    g.activity('ex:illustrate')

    #    used(ex:compose, ex:dataSet1, -,   [ prov:role = "ex:dataToCompose"])
    g.used('ex:compose', 'ex:dataSet1', other_attributes={'prov:role': "ex:dataToCompose"})
    #    used(ex:compose, ex:regionList, -, [ prov:role = "ex:regionsToAggregateBy"])
    g.used('ex:compose', 'ex:regionList', other_attributes={'prov:role': "ex:regionsToAggregateBy"})
    #    wasGeneratedBy(ex:composition, ex:compose, -)
    g.wasGeneratedBy('ex:composition', 'ex:compose')

    #    used(ex:illustrate, ex:composition, -)
    g.used('ex:illustrate', 'ex:composition')
    #    wasGeneratedBy(ex:chart1, ex:illustrate, -)
    g.wasGeneratedBy('ex:chart1', 'ex:illustrate')

    #    wasGeneratedBy(ex:chart1, ex:compile,  2012-03-02T10:30:00)
    g.wasGeneratedBy('ex:chart1', 'ex:compile', '2012-03-02T10:30:00')
    #    wasGeneratedBy(ex:chart2, ex:compile2, 2012-04-01T15:21:00)
    #
    #
    #    agent(ex:derek, [ prov:type="prov:Person", foaf:givenName = "Derek",
    #           foaf:mbox= "<mailto:derek@example.org>"])
    g.agent('ex:derek', {
        'prov:type': PROV["Person"], 'foaf:givenName': "Derek", 'foaf:mbox': "<mailto:derek@example.org>"
    })
    #    wasAssociatedWith(ex:compose, ex:derek, -)
    g.wasAssociatedWith('ex:compose', 'ex:derek')
    #    wasAssociatedWith(ex:illustrate, ex:derek, -)
    g.wasAssociatedWith('ex:illustrate', 'ex:derek')
    #
    #    agent(ex:chartgen, [ prov:type="prov:Organization",
    #           foaf:name = "Chart Generators Inc"])
    g.agent('ex:chartgen', {'prov:type': PROV["Organization"], 'foaf:name': "Chart Generators Inc"})
    #    actedOnBehalfOf(ex:derek, ex:chartgen, ex:compose)
    g.actedOnBehalfOf('ex:derek', 'ex:chartgen', 'ex:compose')
    #    wasAttributedTo(ex:chart1, ex:derek)
    g.wasAttributedTo('ex:chart1', 'ex:derek')

    #    wasGeneratedBy(ex:dataSet2, ex:correct, -)
    g.wasGeneratedBy('ex:dataSet2', 'ex:correct')
    #    used(ex:correct, ex:dataSet1, -)
    g.used('ex:correct', 'ex:dataSet1')
    #    wasDerivedFrom(ex:dataSet2, ex:dataSet1, [prov:type='prov:Revision'])
    g.wasDerivedFrom('ex:dataSet2', 'ex:dataSet1', other_attributes={'prov:type': PROV['Revision']})
    #    wasDerivedFrom(ex:chart2, ex:dataSet2)
    g.wasDerivedFrom('ex:chart2', 'ex:dataSet2')

    #    wasDerivedFrom(ex:blogEntry, ex:article, [prov:type='prov:Quotation'])
    g.wasDerivedFrom('ex:blogEntry', 'ex:article', other_attributes={'prov:type': PROV['Quotation']})
    #    specializationOf(ex:articleV1, ex:article)
    g.specializationOf('ex:articleV1', 'ex:article')
    #    wasDerivedFrom(ex:articleV1, ex:dataSet1)
    g.wasDerivedFrom('ex:articleV1', 'ex:dataSet1')

    #    specializationOf(ex:articleV2, ex:article)
    g.specializationOf('ex:articleV2', 'ex:article')
    #    wasDerivedFrom(ex:articleV2, ex:dataSet2)
    g.wasDerivedFrom('ex:articleV2', 'ex:dataSet2')

    #    alternateOf(ex:articleV2, ex:articleV1)
    g.alternateOf('ex:articleV2', 'ex:articleV1')

    # endDocument
    return g

prov_document = primer_example()

# Store the document to ProvStore:
#   - the public parameter is optional and defaults to False
provneo4j_api.document.create(prov_document, name="Primer Example")

# => This will store the document and return a ProvStore Document object



