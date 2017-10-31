#!/bin/bash

usage()
{
echo "USAGE:
./do_weeks.sh <raspberryprov_rootdir> <outdir>

    <raspberryprov_rootdir>: root of raspberry_prov.git (../)
    <outdir>: (non-existent) directory to put the output from this script
"
exit 1
}

doit()
{

for MODE in 0 1 2
do
  ./thermostat 672 $1 ${MODE}
  cd -
  cd ${CONV_DIR}
  python3 ctf_to_prov.py ../ctf
  cd -
  mv ${CONV_DIR}/output.json ${OUT_DIR}/${1}-${MODE}.json
  cd ${TEMP_DIR}
done

}

if [[ -z $1 || ! -d $1 ]]; then
    echo "ERROR: bad arg for raspberryprov_rootdir"
    usage
fi

if [[ -z $2 || -d $2 ]]; then
    echo "ERROR: bad arg for outdir"
    usage
fi


RASPBERRYPROV_ROOTDIR=$1
OUT_DIR=$2

TEMP_DIR=${RASPBERRYPROV_ROOTDIR}/samples/temperature
CONV_DIR=${RASPBERRYPROV_ROOTDIR}/converter

cd ${TEMP_DIR}
if [ ! -d data ]; then
    echo "ERROR: data does not exist!"
    cd -
    exit 1
fi
cd -

mkdir ${OUT_DIR}
cd ${OUT_DIR}
    mkdir data
cd -


JULY_2012=735080
let AUGUST_2012=${JULY_2012}+31
let SEPTEMBER_2012=${AUGUST_2012}+31
let OCTOBER_2012=${SEPTEMBER_2012}+30
let NOVEMBER_2012=${OCTOBER_2012}+31
let DECEMBER_2012=${NOVEMBER_2012}+30
let JANUARY_2013=${DECEMBER_2012}+31
let FEBRUARY_2013=${JANUARY_2013}+31
let MARCH_2013=${FEBRUARY_2013}+28
let APRIL_2013=${MARCH_2013}+31
let MAY_2013=${APRIL_2013}+30
let JUNE_2013=${MAY_2013}+31
let JULY_2013=${JUNE_2013}+30

cd ${TEMP_DIR}

for occ in {1..24}
do
    echo "Running Occupant ${occ}"

    # The first day in the dataset is July 1, 2012 starting on 735080.000000.
    # The final day in the dataset is June 30, 2013 ending on 735444.999999.
    # Every day is an increment by 1.00000.
    date=${JULY_2012}
    for ((week=1;week<54;week+=1))
    do
      doit data/thermostat_sim_occupant_${occ}_week_${week}.csv
    done
done

cd -

