#!/bin/bash

usage()
{
echo "USAGE:
./do_weeks.sh <raspberryprov_rootdir> <outdir>

    <raspberryprov_rootdir>: root of raspberry_prov.git (../)
    <outdir>: (non-existent) directory to put the output from this script
    <datadir>: directory that contains the temperature .json files
"
exit 1
}

doit()
{

  file_name=${SCRIPT_DIR}/test.py
  fooShell=$(python3 ${SCRIPT_DIR}/test.py $1 $2)
  echo "${fooShell}" >> $3
}

if [[ -z $1 || ! -d $1 ]]; then
    echo "ERROR: bad arg for raspberryprov_rootdir"
    usage
fi

if [[ -z $2 || -d $2 ]]; then
    echo "ERROR: bad arg for outdir"
    usage
fi

if [[ -z $3 || ! -d $3 ]]; then
    echo "ERROR: bad arg for datadir"
    usage
fi

RASPBERRYPROV_ROOTDIR=$1
OUT_DIR=$2
DATA_DIR=$3

SCRIPT_DIR=${RASPBERRYPROV_ROOTDIR}/graph_similarity

mkdir ${OUT_DIR}
cd ${OUT_DIR}
  touch output.txt
  cd -

# echo "Running Occupant ${occ}"
echo "Running Occupant 1, Mode 0"
# Function calls test.py with the json files of an occupant 2 at a time, incrementing
# by 1 every time.
for ((week=1;week<53;week+=1))
do
	echo "Comparing Weeks ${week} and $((week+1))"
  	doit ${DATA_DIR}/thermostat_sim_occupant_1_week_${week}.csv-0.json ${DATA_DIR}/thermostat_sim_occupant_1_week_$((week+1)).csv-0.json ${OUT_DIR}/output.txt
done