from graphtovector import GraphtoVector
import sys
from cosine_similarity import cos_sim
import numpy as np



'''This file is used to test the graph to vector class'''
def getCosSim(file1, file2):
	graphtovec = GraphtoVector([file1,file2])
	vecList = graphtovec.genVectorSet()
	'''uncomment code below to perform cosine similarity between two vectors'''
	v_x = np.array(vecList[0]) 
	v_y = np.array(vecList[1])

	return str(cos_sim(v_x, v_y))