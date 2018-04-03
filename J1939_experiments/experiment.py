#!/usr/bin/python

# Authors:
#   Gedare Bloom

from __future__ import print_function

import csv
import getopt
import itertools
import os
import sys

import numpy as np

sys.path.append(os.path.join("..", "graph_similarity"))
from graph_driver import calculate_similarity

sys.path.append(os.path.join("..", "pruning_implementation"))
from pruning import get_pruned_data
from pruning import create_stream_file

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
                        0   None\n\
                        1   FIFO\n\
                        2   J1939 Priority\n\
  -t --threshold    threshold below which anomalies are detected [0.70]\n\
  -l --length       max length of trace before pruning (if prune > 0) [1024]\n\
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

def prune_trace(prune, ctf, pctf, length):
    if not os.path.exists(pctf):
        print("Error: " + str(pctf) + " subdirectory does not exist")
        exit(1)
    my_deque = get_pruned_data(ctf, length)
    create_stream_file(pctf, my_deque)

def generate_trace(temp_filename, prune, length):
    if not os.path.exists("ctf"):
        print("Error: ctf subdirectory does not exist")
        exit(1)
    canbus_exe = os.path.join("..", "samples", "canbus", "canbus")
    if not os.path.exists(canbus_exe):
        print("Error: canbus executable not found at: " + canbus_exe)
        exit(1)
    os.system(canbus_exe + " " + temp_filename)
    if prune > 0:
        prune_trace(prune, "ctf", "pctf", length)

def convert_trace_to_prov(output_dir, tag, prune):
    # FIXME: import ctf_to_prov?
    ctf = None
    converter = os.path.join("..", "converter", "ctf_to_prov.py")
    if not os.path.exists(converter):
        print("Error: ctf_to_prov.py not found at: " + converter)
        exit(1)
    if prune > 0:
        ctf = os.path.join("..", os.path.basename(os.getcwd()), "pctf")
    else:
        ctf = os.path.join("..", os.path.basename(os.getcwd()), "ctf")
    os.system("python3 " + converter + " " + ctf)
    filename = os.path.join(output_dir, tag + ".json")
    os.rename("output.json", filename)
    return filename

def generate_prov(output_dir, log_format, windows, window_count, train_count, prune, max_trace_length, verbose):
    train_files = []
    test_files = []
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
        generate_trace(temp_filename, prune, max_trace_length)
        f =  convert_trace_to_prov(output_dir, tag + str(index), prune)
        if index >= train_count:
            test_files.append(f)
        else:
            train_files.append(f)
        index = index + 1
    return (train_files, test_files)

def get_ground_truth(input_filename, window_size, window_count, train_count):
    anom_windows = []
    infile_base = os.path.basename(input_filename)
    infile_root = os.path.splitext(infile_base)[0]
    s = infile_root.split("_")
    injection_base_index = int(s[3])
    injection_window = int(injection_base_index / window_size)
    injection_window2 = int((injection_base_index + 10) / window_size)
    iw_base = injection_window - train_count
    iw_end = injection_window2 - train_count
    anom_windows = [i == iw_base or i == iw_end for i in range(window_count - train_count)]
    return anom_windows 

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def validate_args(input_filename, output_dir, log_format,
        disregard, numevts, fraction, prune):
    if not os.path.exists(input_filename):
        eprint("Error: input file not found: " + input_filename)
        return False

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    if log_format is None:
        eprint("Error: missing required argument to specify the log format.")
        return False

    if log_format != "CAN" and log_format != "J1939":
        eprint("Error: invalid log format specified: " + log_format)
        return False

    if numevts is not None and numevts < 1:
        eprint("Error: invalid numevts: " + str(numevts))
        return False

    if disregard < 1 or (numevts is not None and disregard > numevts):
        eprint("Error: invalid disregard: " + str(disregard))
        return False

    if fraction <= 0 or fraction > 1:
        eprint("Error: invalid fraction: " + str(fraction))
        return False

    if prune < 0 or prune > 2:
        eprint("Error: invalid prune: " + str(prune))
        return False

    return True

def main():
    # Default Parameters
    input_filename = "driving_data.csv"
    output_dir = "out"
    disregard = 2
    numevts = None
    fraction = 1.0
    prune = 0
    threshold = 0.70
    trace_length = 1024
    verbose = False

    log_format = "J1939"

    # Parse command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvi:o:d:n:f:p:t:l:",
            ["help", "verbose", "input=", "output_dir=",
             "disregard=", "numevts=", "fraction=", "prune=",
             "threshold=", "length="])
    except (getopt.GetoptError, err):
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
        elif opt in ("-t", "--threshold"):
            threshold = float(arg)
        elif opt in ("-l", "--length"):
            trace_length = int(arg)
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

    (train_files, test_files) = generate_prov(output_dir, log_format, windows, wc, train_count, prune, trace_length, verbose)
    scores = calculate_similarity(train_files, test_files)

    # Anomaly Detection. scores is a list of lists containing the similarity
    # of each test window (from test_files) compared to every training window
    # (from train_files). An anomaly is detected in a test window if its score
    # is below a threshold for all training windows.
    max_scores = [max(x) for x in scores]
    detected_anomalies = [x <= threshold for x in max_scores]
    real_anomalies = get_ground_truth(input_filename, window_size, wc, train_count)

    output_filename = os.path.join(output_dir, str(prune), str(fraction),
            os.path.splitext(os.path.basename(input_filename))[0] + ".txt")

    with open(output_filename, 'w') as scores_file:
        print(scores, file=scores_file)
        print(max_scores, file=scores_file)
        print(detected_anomalies, file=scores_file)
        print(real_anomalies, file=scores_file)

    if verbose is True:
        print(scores)
        print(max_scores)
        print(detected_anomalies)
        print(real_anomalies)

    TN = TP = FN = FP = 0
    for w in range(wc - train_count):
        if detected_anomalies[w] == False and real_anomalies[w] == False:
             TN += 1
        elif detected_anomalies[w] == True and real_anomalies[w] == True:
             TP += 1
        elif detected_anomalies[w] == False and real_anomalies[w] == True:
             FN += 1
        elif detected_anomalies[w] == True and real_anomalies[w] == False:
             FP += 1

    print("%d\t%d\t%d\t%d" % (TN, TP, FN, FP))



if __name__ == '__main__':
    main()
