import argparse
import sys
import os
import errno
import threading
from graph_driver import calculate_similarity


def doIt(occupant, out_dir, data_dir, mode):
  print("Running Occupant %d, Mode %d" % (occupant, mode))
  output_file = os.path.join(out_dir, "occupant_%d_mode_%d.txt" % (occupant, mode))
  if os.path.exists(output_file):
    print("Error: File %s already exists, delete it" % (output_file))
    return -1
  with open(output_file, 'w') as file:
    for week in range(1, 53):
      arg1 = os.path.join(
          data_dir, "thermostat_sim_occupant_%d_week_%d.csv-%d.json" % (occupant, week, mode))
      arg2 = os.path.join(
          data_dir, "thermostat_sim_occupant_%d_week_%d.csv-%d.json" % (occupant, week + 1, mode))
      result = calculate_similarity(arg1, arg2)[0]
      file.write(result + "\n")


def start(out_dir, data_dir, occ):
  threads = []
  for mode in range(0, 3):
    t = threading.Thread(target=doIt, args=(occ, out_dir, data_dir, mode))
    threads.append(t)
    t.start()


def main(args):
  RASPBERRYPROV_ROOTDIR = args.prov_rootdir
  OUT_DIR = args.outdir
  DATA_DIR = args.data_dir
  OCC = args.occ
  MODE = args.mode
  if not os.path.isdir(RASPBERRYPROV_ROOTDIR):
    print("Path doesn't exist %s , please provide a valid root" %
          (RASPBERRYPROV_ROOTDIR))
    return -1
  if not os.path.isdir(DATA_DIR):
    print("Path doesn't exist %s , please provide a valid root" % (DATA_DIR))
    return -1
  try:
    # If directory has not yet been created
    os.makedirs(OUT_DIR)
  except OSError as e:
    # If directory has already been created or is inaccessible
    if not os.path.exists(OUT_DIR):
      sys.exit("Error creating %s" %(OUT_DIR))
  if args.all_modes:
    start(OUT_DIR, DATA_DIR, OCC)
  else:
    doIt(OCC, OUT_DIR, DATA_DIR, MODE)


if __name__ == "__main__":
  parser=argparse.ArgumentParser()
  parser.add_argument("prov_rootdir", help="root of raspberry_prov.git (../)")
  parser.add_argument("outdir", help="directory to put the output from this script")
  parser.add_argument("data_dir", help="directory to .json data")
  parser.add_argument("--occ", type=int, default=1, choices=set(range(1,26)),
    help="which occupant (between 1 - 24) to do the comparisons on")
  parser.add_argument("--mode", type=int, default=1, choices=set((0,1,2)),
    help="Which mode do use for the comparisons (0=off, 1=heating, 2=cooling")
  parser.add_argument("--all_modes", default=False, action="store_true",
    help="Compare all the modes")
  args = parser.parse_args()
  main(args)
    # this was run as a main script
