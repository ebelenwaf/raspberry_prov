#!/usr/bin/python

# Authors:
#   David Hill, Jr.

from experiment import *
import numpy as np


def usage():
   print "Usage: injection.py -[hvi:o:d:p:n]\n\
 -h --help         print this help\n\
 -v --verbose      print more information [False]\n\
 -i --input        input log filename [driving_data.csv]\n\
 -o --output       output log filename [anomalous_data.csv]\n\
 -d --disregard    denominator of 1/d % events not subject to injection [4]\n\
					   Note: d must match that used during injection, and\n\
					   the max window size is n/d.\n\
-p --injection-point [0] \n\
-n --num-injections [10] \n\
"


def min_time_gap(gaps):
	""" This function finds the minimum time gap in the gaps data set in microseconds. """
	return min(gaps)

def max_time_gap(gaps):
	""" This function finds the maximum time gap in the gaps data set in microseconds. """
	return max(gaps)

def avg_time_gap(gaps):
	""" This function finds the average time gap of the gaps data set in microseconds. """
	return int(np.mean(gaps))

def fabricate_msg(mal_str, original_ts, offset):

	mal_message = mal_str.split(",")
	new_ts = original_ts + offset
	mal_message[0] = str(microseconds_to_HHMMSSmmuu(new_ts))

	return mal_message


def injectMsg(in_file, disregard, gap_to_inject ,mal_str, num_msg):
	""" This method injects a user specified amount of malicious J1939 messages into a given data set. 
		Parameters:
		in-file - The desired input data file name
		disregard - The desired portion of the data set that should not be subject to injection. Calculated as 1/disregard.
					+ EX: disregard = 4
						  1/4 of the file will be disregarded
		gap_to_inject - This parameter specifies which gap in the data set of size min_gap * 12 to inject the data.
					+ EX: gap_to_inject = 1
					      The first gap after the disregard of size min_gap * 12 or greater will be injected.
		mal_str - The malicious string the user wants to inject.
		num_msg - The number of messages desired for injection.

	"""

	anom_data = []

	data = read_lists_from_CSV(in_file)

	if gap_to_inject <= 0:
		return -1, data

	timestamp_rows = [ HHMMSSmmuu_ts_to_microseconds(row[0]) for row in data]
	start_idx = int((1.0/disregard) * len(data))

	gaps = [(timestamp_rows[row+1]) - timestamp_rows[row] for row in range(len(data)-1)]

	avg_gap = int(avg_time_gap(gaps))
	min_gap = min_time_gap(gaps)
	max_gap = max_time_gap(gaps)

	desired_gaps_idx = []

	for event_idx in range(len(timestamp_rows)-1):
		if timestamp_rows[event_idx+1] - timestamp_rows[event_idx] >= min_gap * 12 and event_idx > start_idx:
			desired_gaps_idx.append(event_idx)


	injected_idx = -1

	for x in range(len(data)-1):

		if x <= start_idx:
			anom_data.append(data[x])
		
		elif x > start_idx:
			try:
				if x == desired_gaps_idx[gap_to_inject]:

					curr_ts = timestamp_rows[x]
					injected_idx = x + 1

					for y in range(num_msg):
						curr_ts	+= (timestamp_rows[x+1]-timestamp_rows[x])/12
						anom_data.append(fabricate_msg(mal_str, curr_ts, (timestamp_rows[x+1]-timestamp_rows[x])/12))

				else:
					anom_data.append(data[x])

			except:
				print "ERROR: Cannot inject message. gap_to_inject is either out of range."
				return -1, data

		else:
			anom_data.append(data[x])
	
	
	return injected_idx, anom_data

def main():

	# Default Parameters
	in_file = 'driving_data.csv'
	disregard = 4
	inject_point = 0
	malicious_msg = '1,2,C000003x,C000003x,CAN - EXT,8,01 41 A0 FF FF FF FF FF,Tx'
	output = 'anomalous_data.csv'
	number_injections = 10
	verbose = False


	
	# Parse command line arguments

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hvi:o:d:p:n",
			["help", "verbose", "input=", "output=",
			 "disregard=", "injection-point=", "num-injections="])
	
	except getopt.GetoptError, err:
		print(str(err))
		usage()
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit(0)
		elif opt in ("-v", "--verbose"):
			verbose = True
		elif opt in ("-i", "--input"):
			input_filename = arg
		elif opt in ("-o", "--output"):
			output = arg
		elif opt in ("-d", "--disregard"):
			disregard = int(arg)
		elif opt in ("-p", "--inject_point"):
			inject_point = int(arg)
		elif opt in ("-n", "--number_injections"):
			number_injections = int(arg)
		else:
			print("Unhandled option: " + opt + "\n")
			usage()
			sys.exit(2)

	index, malData = injectMsg(in_file, disregard, inject_point, malicious_msg, number_injections )
	if index >= 0:
		write_lists_to_CSV(output, malData)

	if verbose == True:
		print " Messages injected at index %d " % index





if __name__ == '__main__':
	main()
