# Graph Similarity

## Getting started
The files contained in this folder are described below:

* EdgeList.py: Creates a list of edges for each graph from a json output and a unique list of edges given a set of edges (also know as global edge list).
* edge.py: Creates an edge object with source, destination node and label fields.
* graphtovector.py: Generates the vector representation of a graph(s) given a set of edgelist.
* test.py: test function for graphtovector.py
* compare_weeks.py: Used to generate a file containing cosine similiarity values for a given occupant and mode for 52 weeks.

## Prerequisite

In order to run the code here, you need to install the following software

* python >= 2.7, python3
* numpy



## Installing

* To execute the functionalities of the graphtovector class, compile `test.py` including the file location of the json object containing the provenance representation.  `python3 test.py prov.json output.json`. This returns a set of vectors for each json file specified.



## How to run compare_weeks.py
This script has 3 positional arguments and 3 optional arguments.

Positional:
root_dir
output_dir
data_dir

Optional:
--occ
--mode
--all_modes

You can run python3 compare_weeks.py -h for more clarification.

example command that will run comparisions for occupant 1 and mode 1:
```
	python3 compare_weeks.py ~/raspberry_prov/ ~/raspberry_prov/results/ ~/raspberry_prov/data/
  ```







