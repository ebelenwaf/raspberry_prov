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
    return max(gaps)

def max_time_gap(gaps):
	""" This function finds the maximum time gap in the gaps data set in microseconds. """
	return min(gaps)

def avg_time_gap(gaps):
	""" This function finds the average time gap of the gaps data set in microseconds. """
 	return int(np.mean(gaps))

def injectMsg(in_file, out_file, disregard, mal_str):
 	""" """

 	mal_message = mal_str.split(",")

 	data = read_lists_from_CSV(in_file)
 	timestamp_rows = [ HHMMSSmmuu_ts_to_microseconds(row[0]) for row in data]

 	gaps = [(timestamp_rows[row+1]) - timestamp_rows[row] for row in range(len(data)-1)]
 	avg_gap = int(avg_time_gap(gaps))
 	min_gap = min_time_gap(gaps)
 	max_gap = max_time_gap(gaps)

 	print microseconds_to_HHMMSSmmuu(timestamp_rows[0])

 	

 	
 	

 	return out_file

def main():

	#usage()
	
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

	injectMsg('driving_data.csv','output_data.csv',4,'1,2,C000003x,C000003x,CAN - EXT,8,01 41 A0 FF FF FF FF FF,Tx')
	

	





if __name__ == '__main__':
    main()