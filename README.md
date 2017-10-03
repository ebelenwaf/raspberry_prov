# raspberry_prov

## Getting started
This instruction will get the project up and running on your local machine. There are three folders contained in the raspberry_prov folder. These folders are described below:

* babelt_work: Contains code that extracts events from ctf stream file located in `ctf/` and converts these events to PROV-DM format. Also contains code for storing provenance into neo4j database.
* ctf: contains metadata and stream file fromt trace collection.




## Prerequisite

In order to run the sample `sample_c.c` application, you need to install the following software

* GCC (C- Compiler)
* barectf
* babeltrace 3.0
* python >= 2.7
* Neo4j 
* make


## Installing

* To compile the sample `sample_c.c` program, use the command 'make' and to clean the directory, usually before compiling a new version, use the command 'make clean'. The 'make' command generates the stream file contained in the ctf folder. This file contains events trace from the sample `sample_c.c` application. 

* To convert trace events contained in the stream file to human readable PROV-DM format, run the python script `babel_trace_2.py` located in the babelt_work folder. This generates a json file `output.json` containing the provenance conversion.


* To store PROV-DM file in the neo4j database, run python script `tester.py` contained in babelt_work folder. This also produces a pdf file `output.pdf` containing the provenance representation.






