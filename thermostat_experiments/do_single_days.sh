#!/bin/bash

usage()
{
echo "USAGE:
./do_single_days.sh <raspberryprov_rootdir> <outdir>

    <raspberryprov_rootdir>: root of raspberry_prov.git (../)
    <outdir>: (non-existent) directory to put the output from this script
"
exit 1
}

doit()
{

for MODE in 0 1 2
do
  ./thermostat 96 $1 ${MODE}
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
    mkdir data/jul_2012
    mkdir data/aug_2012
    mkdir data/sep_2012
    mkdir data/oct_2012
    mkdir data/nov_2012
    mkdir data/dec_2012
    mkdir data/jan_2013
    mkdir data/feb_2013
    mkdir data/mar_2013
    mkdir data/apr_2013
    mkdir data/may_2013
    mkdir data/jun_2013
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
    while [ ${date} -lt ${AUGUST_2012} ]
    do
      if [ -d data/jul_2012 ]; then
        doit data/jul_2012/thermostat_sim_occupant_${occ}_jul_${date}.csv
      fi
      let date=${date}+1
    done

    while [ ${date} -lt ${SEPTEMBER_2012} ]
    do
      if [ -d data/aug_2012 ]; then
        doit data/aug_2012/thermostat_sim_occupant_${occ}_aug_${date}.csv
      fi
      let date=${date}+1
    done

    while [ ${date} -lt ${OCTOBER_2012} ]
    do
      if [ -d data/sep_2012 ]; then
        doit data/sep_2012/thermostat_sim_occupant_${occ}_september_${date}.csv
      fi
      let date=${date}+1
    done

    while [ ${date} -lt ${NOVEMBER_2012} ]
    do
      if [ -d data/oct_2012 ]; then
        doit data/oct_2012/thermostat_sim_occupant_${occ}_oct_${date}.csv
      fi
      let date=${date}+1
    done

    while [ ${date} -lt ${DECEMBER_2012} ]
    do
      if [ -d data/nov_2012 ]; then
        doit data/nov_2012/thermostat_sim_occupant_${occ}_nov_${date}.csv
      fi
      let date=${date}+1
    done

    while [ ${date} -lt ${JANUARY_2013} ]
    do
      if [ -d data/dec_2012 ]; then
        doit data/dec_2012/thermostat_sim_occupant_${occ}_dec_${date}.csv
      fi
      let date=${date}+1
    done

    while [ ${date} -lt ${FEBRUARY_2013} ]
    do
      if [ -d data/jan_2013 ]; then
        doit data/jan_2013/thermostat_sim_occupant_${occ}_jan_${date}.csv
      fi
      let date=${date}+1
    done

    while [ ${date} -lt ${MARCH_2013} ]
    do
      if [ -d data/feb_2013 ]; then
        doit data/feb_2013/thermostat_sim_occupant_${occ}_feb_${date}.csv
      fi
      let date=${date}+1
    done

    while [ ${date} -lt ${APRIL_2013} ]
    do
      if [ -d data/mar_2013 ]; then
        doit data/mar_2013/thermostat_sim_occupant_${occ}_mar_${date}.csv
      fi
      let date=${date}+1
    done

    while [ ${date} -lt ${MAY_2013} ]
    do
      if [ -d data/apr_2013 ]; then
        doit data/apr_2013/thermostat_sim_occupant_${occ}_apr_${date}.csv
      fi
      let date=${date}+1
    done

    while [ ${date} -lt ${JUNE_2013} ]
    do
      if [ -d data/may_2013 ]; then
        doit data/may_2013/thermostat_sim_occupant_${occ}_may_${date}.csv
      fi
      let date=${date}+1
    done

    while [ ${date} -lt ${JULY_2013} ]
    do
      if [ -d data/jun_2013 ]; then
        doit data/jun_2013/thermostat_sim_occupant_${occ}_jun_${date}.csv
      fi
      let date=${date}+1
    done

done

cd -

