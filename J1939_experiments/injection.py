#!/usr/bin/python

# Authors:
#   David Hill, Jr.

from experiment import *
import numpy as np


def usage():
   print "Usage: injection.py -[hvi:o:d:n:f:p:]\n\
 -h --help         print this help\n\
 -v --verbose      print more information [False]\n\
 -i --input        input log filename [driving_data.csv]\n\
 -o --output       output log filename [injection_driving_data.csv]\n\
 -d --disregard    denominator of 1/d % events not subject to injection [2]\n\
					   Note: d must match that used during injection, and\n\
					   the max window size is n/d.\n\
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

def injectMsg(in_file, disregard, gap_to_inject ,mal_str, num_msg ,intensity):

	inject = True

	if gap_to_inject <= 0:
		inject = False

	mal_message = mal_str.split(",")
	anom_data = []

	injected_idx = None

	data = read_lists_from_CSV(in_file)
	timestamp_rows = [ HHMMSSmmuu_ts_to_microseconds(row[0]) for row in data]
	start_idx = int((1.0/disregard) * len(data))

	gaps = [(timestamp_rows[row+1]) - timestamp_rows[row] for row in range(len(data)-1)]

	avg_gap = int(avg_time_gap(gaps))
	min_gap = min_time_gap(gaps)
	max_gap = max_time_gap(gaps)

	desired_gaps_idx = []

	for event_idx in range(len(timestamp_rows)-1):
		if timestamp_rows[event_idx+1] - timestamp_rows[event_idx] >= min_gap * 12:
			desired_gaps_idx.append(event_idx)


	inject_failed = False

	for x in range(len(data)-1):

		if x <= start_idx:
			anom_data.append(data[x])
		
		elif x > start_idx:
			try:
				if x == desired_gaps_idx[gap_to_inject]:

					curr_ts = timestamp_rows[x]
					injected_idx = x + 1

					for y in range(num_msg):
						curr_ts = curr_ts + (timestamp_rows[x+1]-timestamp_rows[x])/12
						mal_message[0] = microseconds_to_HHMMSSmmuu(curr_ts)
						print mal_message
						anom_data.append(mal_message)

				else:
					print(data[x])
					anom_data.append(data[x])

			except:
				inject_failed = True
				print "ERROR: Cannot inject message. gap_to_inject is either out of range or 0."
				return -1

		else:
			anom_data.append(data[x])
	
	print injected_idx
	return anom_data

def main():
	
	# Parse command line arguments
	"""try:
		opts, args = getopt.getopt(sys.argv[1:], "hvi:o:d:n:f:p:",
			["help", "verbose", "input=", "output_dir=",
			 "disregard="])
	
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
		elif opt in ("-o", "--output_dir"):
			output_dir = arg
		elif opt in ("-d", "--disregard"):
			disregard = int(arg)
		elif opt in ("-n", "--numevts"):
			numevts = int(arg)
		elif opt in ("-f", "--fraction"):
			fraction = float(arg)
		elif opt in ("-p", "--prune"):
			prune = int(arg)
		else:
			print("Unhandled option: " + opt + "\n")
			usage()
			sys.exit(2)

	if not validate_args(input_filename, output_dir,
			log_format,
			disregard, numevts, fraction, prune):
		usage()
		sys.exit(1)"""

malData = injectMsg('driving_data.csv',4, 2000, '1,2,C000003x,C000003x,CAN - EXT,8,01 41 A0 FF FF FF FF FF,Tx', 10 , 2)
write_lists_to_CSV('test.csv', malData)



if __name__ == '__main__':
	main()
