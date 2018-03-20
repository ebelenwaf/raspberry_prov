#!/usr/bin/python

# Authors:
#   Gedare Bloom
#   David Hill, Jr.

from experiment import *

def min_time_gap(data):
    """ This function finds the minimum time gap in the data set in microseconds. """

    min_gap = data[1][0] - data[0][0]

    for row in range(len(data)-1):
        if data[row + 1][0] - data[row][0] < min_gap:
        	mingap = data[row + 1][0] - data[row][0]

    return min_gap

def max_time_gap(data):
	""" This function finds the maximum time gap in the data set in microseconds. """

	max_gap = data[1][0] - data[0][0]

	for row in range(len(data)-1):
		if data[row + 1][0] - data[row][0] > max_gap:
			max_gap = data[row + 1][0] - data[row][0]

	return max_gap

def avg_time_gap(data):
	""" This function finds the average time gap of the data set in microseconds. """
 	
 	gap_sum = 0

 	for row in range(len(data)-1):
 		gap_sum += (data[row + 1][0] - data[row][0])

 	return gap_sum/(len(data)/2)

def injectMsg():
 	""" """



def main():
 	data = read_lists_from_CSV('driving_data.csv')
 	
 	for row in data:
 		row[0] = HHMMSSmmuu_ts_to_microseconds(row[0])


 	print "Average Gap:", avg_time_gap(data), "microseconds"
 	print "Minimum Gap:", min_time_gap(data), "microseconds"
 	print "Maximum Gap:", max_time_gap(data), "microseconds"





if __name__ == '__main__':
    main()