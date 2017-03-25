# raspberry_prov

## Getting started
This instruction will get the project up and running on your local machine. There are three folders contained in the raspberry_prov folder. These folders are described below:

* babelt_work: Contains code that extracts events from ctf stream file located in `ctf/` and converts these events to PROV-DM format.
* ctf: contains metadata and stream file.
* prov2neo4j: contains code for storing PROV-DM trace in Neo4j graph database.



## Prerequisite

In order to run the sample `temp.c` application, you need to install the following software

* GCC (C- Compiler)
* barectf
* babeltrace 3.0
* python >= 2.7
* Neo4j 
* make


## Installing

* To compile the sample `temp.c` program, use the command 'make' and to clean the directory, usually before compiling a new version, use the command 'make clean'. The 'make' command generates the stream file contained in the ctf folder. This file contains events trace from the sample `temp.c` application. 

* To convert events contained in the stream file to human readable PROV-DM format, run the python script located in the babelt_work folder. 


* To store PROV-DM file, run python script contained in prov2neo4j file.


## License

This project is licensed under the MIT License.



