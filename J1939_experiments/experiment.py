#!/usr/bin/python

# Authors:
#   Gedare Bloom

from __future__ import print_function

import csv
import getopt
import itertools
import os
import sys

def usage():
    print("\
Usage: experiment.py -[hi:o:]\n\
  -h --help         print this help\n\
  -i --input        input filename [driving_data.csv]\n\
  -o --output       output filename [results.txt]\n\
")

def read_lists_from_CSV(filename):
    """Converts a CSV file to a list of lists.

    Reads each row of the CSV file identified by filename into a list,
    accumulating all rows into a list-of-lists.

    Args:
        filename: A string identifying a CSV file.

    Returns:
        A list-of-lists containing the rows of the CSV file.

    Raises:
        IOError: An error occurred while reading the CSV file.
    """
    data = []

    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = [row for row in reader]

    return data
            
def write_lists_to_CSV(filename, data):
    """Generates a CSV file from a list of lists.

    Args:
        filename: A string identifying a CSV file.
        data: List of rows to write to the file.
    """
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def trim_J1939(data):
    data[:] = [x for x in data if len(x) > 1 and "00:" in x[0]]

def trim_CAN(data):
    data[:] = [x for x in data if len(x) > 22 and "Line" not in x[0]]

def trim_data(data, log_format):
    """Removes rows of data that do not contain log entries."""
    if log_format == "J1939":
        trim_J1939(data)
    elif log_format == "CAN":
        trim_CAN(data)
    else:
        assert False, "Error: unrecognized log format: " + log_format

def HHMMSSmmuu_ts_to_microseconds(timestamp):
    """Converts a timestamp in HH:MM:SS:mm:uu format to microseconds."""
    ts = [int(x) for x in timestamp.split(":")]
    return (((ts[0]*60+ts[1])*60+ts[2])*1000+ts[3])*1000+ts[4]

def s_to_microseconds(s_time):
    """Converts a fractional second timestamp to fractional microseconds."""
    return float(s_time)*1000.0*1000.0

def generate_trace_metadata_J1939(data):
    td = []
    for r in data:
        mu_time = HHMMSSmmuu_ts_to_microseconds(r[0])
        x = list([mu_time, r[1], r[2]])
        x.extend(r[6].split())
        td.append(x)
    return td

def generate_trace_metadata_CAN(data):
    td = []
    for r in data:
        mu_time = int(round(s_to_microseconds(r[1])))
        x = list([mu_time, r[7], r[9]])
        x.extend(r[12:19])
        td.append(x)
    return td

def generate_trace_metadata(data, log_format):
    """Extracts timestamp, id, and payload from each row of data."""
    if log_format == "J1939":
        return generate_trace_metadata_J1939(data)
    elif log_format == "CAN":
        return generate_trace_metadata_CAN(data)
    else:
        assert False, "Error: unrecognized log format: " + log_format

def validate_args(input_filename, output_filename, log_format):
    if not os.path.exists(input_filename):
        print("Error: input file not found: " + input_filename + "\n")
        return False

    if os.path.exists(output_filename):
        print("Warning: will overwrite existing output file: "
                + output_filename + "\n")

    if log_format is None:
        print("Error: missing required argument to specify the log format.\n")
        return False

    if log_format != "CAN" and log_format != "J1939":
        print("Error: invalid log format specified: " + log_format + "\n")
        return False
    return True

def main():
    # Default Parameters
    input_filename = "driving_data.csv"
    output_filename = "test.txt"
    log_format = "J1939"

    # Parse command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:",
            ["help", "input=", "output="])
    except getopt.GetoptError, err:
        print(str(err))
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif opt in ("-i", "--input"):
            input_filename = arg
        elif opt in ("-o", "--output"):
            output_filename = arg
        else:
            print("Unhandled option: " + opt + "\n")
            usage()
            sys.exit(2)

    if not validate_args(input_filename, output_filename, log_format):
        usage()
        sys.exit(1)

    data = read_lists_from_CSV(input_filename)
    trim_data(data, log_format)
    td = generate_trace_metadata(data, log_format)
    write_lists_to_CSV(output_filename, td)

if __name__ == '__main__':
    main()
