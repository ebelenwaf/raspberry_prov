# Graph Similarity

## Getting started
The folders files contained in this folder are described below:

* EdgeList.py: Creates a list of edges for each graph from a json output and a unique list of edges given a set of edges (also know as global edge list).
* edge.py: Creates an edge object with source, destination node and label fields.
* graphtovector.py: Generates the vector representation of a graph(s) given a set of edgelist.
* cosine_similarity.py: Contains cosine similarity function implementation.
* test.py: test function for graphtovector.py


## Prerequisite

In order to run the code here, you need to install the following software

* python >= 2.7, python3
* numpy



## Installing

* To execute the functionalities of the graphtovector class, compile `test.py` including the file location of the json object containing the provenance representation.  `python3 test.py prov.json output.json`. This returns a set of vectors for each json file specified.








