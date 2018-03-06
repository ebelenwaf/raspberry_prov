#!/usr/bin/python

# Authors:
#   Gedare Bloom

from __future__ import print_function

import csv
import getopt
import itertools
import os
import sys

sys.path.append(os.path.join("..", "graph_similarity"))

from graph_driver import getCosSim

def usage():
    print("Usage: experiment.py -[hvi:o:d:n:f:p:]\n\
  -h --help         print this help\n\
  -v --verbose      print more information [False]\n\
  -i --input        input log filename [driving_data.csv]\n\
  -o --output       output directory [out]\n\
  -d --disregard    denominator of 1/d % events not subject to injection [2]\n\
                        Note: d must match that used during injection, and\n\
                        the max window size is n/d.\n\
  -n --numevts      number of events in the input file\n\
  -f --fraction     fraction in (0,1] to subdivide window sizes [1]\n\
  -p --prune        pruning algorithm to use, one of:\n\
                        1   FIFO\n\
                        2   J1939 Priority\n\
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

def generate_trace(temp_filename):
    if not os.path.exists("ctf"):
        print("Error: ctf subdirectory does not exist")
        exit(1)
    canbus_exe = os.path.join("..", "samples", "canbus", "canbus")
    if not os.path.exists(canbus_exe):
        print("Error: canbus executable not found at: " + canbus_exe)
        exit(1)
    os.system(canbus_exe + " " + temp_filename)

def convert_trace_to_prov(output_dir, tag):
    # FIXME: import ctf_to_prov?
    converter = os.path.join("..", "converter", "ctf_to_prov.py")
    if not os.path.exists(converter):
        print("Error: ctf_to_prov.py not found at: " + converter)
        exit(1)
    ctf = os.path.join("..", os.path.basename(os.getcwd()), "ctf")
    os.system("python3.5 " + converter + " " + ctf)
    filename = os.path.join(output_dir, tag + ".json")
    os.rename("output.json", filename)

def generate_prov(output_dir, log_format, windows, window_count, train_count, verbose):
    test_count = window_count - train_count
    temp_filename = os.path.join(output_dir, "temp.txt")

    if verbose is True:
        print("Number of windows: " + str(window_count))
        print("Number of training windows: " + str(train_count))
        print("Number of test windows: " + str(test_count))

    index = 0
    for w in windows[0:window_count]:
        tag = "train"
        if index >= train_count:
            tag = "test"
        if verbose is True:
            print("Generating provenance (" + tag + ") window #" + str(index))
        td = generate_trace_metadata(w, log_format)
        write_lists_to_CSV(temp_filename, td)
        generate_trace(temp_filename)
        convert_trace_to_prov(output_dir, tag + str(index))
        index = index + 1

def calculate_similarity(output_dir, window_count, train_count, verbose):
    scores = []
    test_count = window_count - train_count

    for x in xrange(test_count):
        test = os.path.join(output_dir, "test" + str(x + train_count) + ".json")
        x_scores = []
        for y in xrange(train_count):
            train = os.path.join(output_dir, "train" + str(y) + ".json")
            if verbose is True:
                print("Calculating similarity:" + test + " and " + train)
            x_scores.append(getCosSim(train, test))
        scores.append(x_scores)
    return scores

def validate_args(input_filename, output_dir, log_format,
        disregard, numevts, fraction, prune):
    if not os.path.exists(input_filename):
        print("Error: input file not found: " + input_filename)
        return False

    if os.path.exists(output_dir):
        print("Warning: will overwrite existing files in output directory: "
                + output_dir)
    else:
        os.mkdir(output_dir)

    if log_format is None:
        print("Error: missing required argument to specify the log format.")
        return False

    if log_format != "CAN" and log_format != "J1939":
        print("Error: invalid log format specified: " + log_format)
        return False

    if numevts is not None and numevts < 1:
        print("Error: invalid numevts: " + str(numevts))
        return False

    if disregard < 1 or (numevts is not None and disregard > numevts):
        print("Error: invalid disregard: " + str(disregard))
        return False

    if fraction <= 0 or fraction > 1:
        print("Error: invalid fraction: " + str(fraction))
        return False

    if prune < 1 or prune > 2:
        print("Error: invalid prune: " + str(prune))
        return False

    return True

def main():
    # Default Parameters
    input_filename = "driving_data.csv"
    output_dir = "out"
    disregard = 2
    numevts = None
    fraction = 1.0
    prune = 1

    log_format = "J1939"

    # Parse command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvi:o:d:n:f:p:",
            ["help", "verbose", "input=", "output_dir=",
             "disregard=", "numevts=", "fraction=", "prune="])
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
        sys.exit(1)

    data = read_lists_from_CSV(input_filename)
    trim_data(data, log_format)

    if numevts is None:
        numevts = len(data)

    if numevts < len(data):
        print("Warning: found more than n = " + str(numevts) + " events in "
                + input_filename)

    window_size = int(fraction * float(numevts)/float(disregard))
    windows = [data[x*window_size:(x+1)*window_size] for x in range(int(disregard/fraction))]
    wc = len(windows)

    train_count = int(1.0/fraction)

    if verbose is True:
        print("Number of events: " + str(numevts))
        print("Window size got: " + str(window_size))

    generate_prov(output_dir, log_format, windows, wc, train_count, verbose)
    scores = calculate_similarity(output_dir, wc, train_count, verbose)

    print(scores)
    # TODO: json -> scores

if __name__ == '__main__':
    main()
