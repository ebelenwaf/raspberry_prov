from graphtovector import GraphtoVector
import sys
from cosine_similarity import cos_sim
import numpy as np



'''This file is used to test the graph to vector class'''

graphtovec = GraphtoVector(sys.argv)
vecList = graphtovec.genVectorSet()
print(vecList)
#perform cosine similarity
v_x = np.array(vecList[0]) 
v_y = np.array(vecList[1])

print("\n cosine similarity:"+ str(cos_sim(v_x, v_y))+"\n")