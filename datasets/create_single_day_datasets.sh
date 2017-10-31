#!/bin/bash


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

if [ -d data ]; then
    echo "ERROR: data/ exists, remove it and try again!"
    exit 1
else
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
fi

if [ ! -f LANGEVIN_DATA.txt ]; then
    echo "ERROR: Input file not found -- LANGEVIN_DATA.txt"
    exit 1
fi

echo "Constructing CSV from LANGEVIN_DATA.txt"
awk 'BEGIN{ OFS="," } {print $1,$2,$3,$4,$6,$7,$59,$61}' LANGEVIN_DATA.txt \
  > thermostat_sim.csv

for occ in {1..24}
do
    echo "Processing Occupant ${occ}"
    awk 'BEGIN{ OFS="," ; FS="," } $2 ~ /^'${occ}'.000000$/ {print $0}' \
      thermostat_sim.csv > thermostat_sim_occupant_${occ}.csv

    # The first day in the dataset is July 1, 2012 starting on 735080.000000.
    # The final day in the dataset is June 30, 2013 ending on 735444.999999.
    # Every day is an increment by 1.00000.
    date=${JULY_2012}
    while [ ${date} -lt ${AUGUST_2012} ]
    do
      awk 'BEGIN{ OFS="," ; FS="," } $1 ~ /^'${date}'./ {print $5,$6,$7,$8}' \
        thermostat_sim_occupant_${occ}.csv \
        > data/jul_2012/thermostat_sim_occupant_${occ}_jul_${date}.csv
      let date=${date}+1
    done

    while [ ${date} -lt ${SEPTEMBER_2012} ]
    do
      awk 'BEGIN{ OFS="," ; FS="," } $1 ~ /^'${date}'./ {print $5,$6,$7,$8}' \
        thermostat_sim_occupant_${occ}.csv \
        > data/aug_2012/thermostat_sim_occupant_${occ}_aug_${date}.csv
      let date=${date}+1
    done

    while [ ${date} -lt ${OCTOBER_2012} ]
    do
      awk 'BEGIN{ OFS="," ; FS="," } $1 ~ /^'${date}'./ {print $5,$6,$7,$8}' \
        thermostat_sim_occupant_${occ}.csv \
        > data/sep_2012/thermostat_sim_occupant_${occ}_september_${date}.csv
      let date=${date}+1
    done

    while [ ${date} -lt ${NOVEMBER_2012} ]
    do
      awk 'BEGIN{ OFS="," ; FS="," } $1 ~ /^'${date}'./ {print $5,$6,$7,$8}' \
        thermostat_sim_occupant_${occ}.csv \
        > data/oct_2012/thermostat_sim_occupant_${occ}_oct_${date}.csv
      let date=${date}+1
    done

    while [ ${date} -lt ${DECEMBER_2012} ]
    do
      awk 'BEGIN{ OFS="," ; FS="," } $1 ~ /^'${date}'./ {print $5,$6,$7,$8}' \
        thermostat_sim_occupant_${occ}.csv \
        > data/nov_2012/thermostat_sim_occupant_${occ}_nov_${date}.csv
      let date=${date}+1
    done

    while [ ${date} -lt ${JANUARY_2013} ]
    do
      awk 'BEGIN{ OFS="," ; FS="," } $1 ~ /^'${date}'./ {print $5,$6,$7,$8}' \
        thermostat_sim_occupant_${occ}.csv \
        > data/dec_2012/thermostat_sim_occupant_${occ}_dec_${date}.csv
      let date=${date}+1
    done

    while [ ${date} -lt ${FEBRUARY_2013} ]
    do
      awk 'BEGIN{ OFS="," ; FS="," } $1 ~ /^'${date}'./ {print $5,$6,$7,$8}' \
        thermostat_sim_occupant_${occ}.csv \
        > data/jan_2013/thermostat_sim_occupant_${occ}_jan_${date}.csv
      let date=${date}+1
    done

    while [ ${date} -lt ${MARCH_2013} ]
    do
      awk 'BEGIN{ OFS="," ; FS="," } $1 ~ /^'${date}'./ {print $5,$6,$7,$8}' \
        thermostat_sim_occupant_${occ}.csv \
        > data/feb_2013/thermostat_sim_occupant_${occ}_feb_${date}.csv
      let date=${date}+1
    done

    while [ ${date} -lt ${APRIL_2013} ]
    do
      awk 'BEGIN{ OFS="," ; FS="," } $1 ~ /^'${date}'./ {print $5,$6,$7,$8}' \
        thermostat_sim_occupant_${occ}.csv \
        > data/mar_2013/thermostat_sim_occupant_${occ}_mar_${date}.csv
      let date=${date}+1
    done

    while [ ${date} -lt ${MAY_2013} ]
    do
      awk 'BEGIN{ OFS="," ; FS="," } $1 ~ /^'${date}'./ {print $5,$6,$7,$8}' \
        thermostat_sim_occupant_${occ}.csv \
        > data/apr_2013/thermostat_sim_occupant_${occ}_apr_${date}.csv
      let date=${date}+1
    done

    while [ ${date} -lt ${JUNE_2013} ]
    do
      awk 'BEGIN{ OFS="," ; FS="," } $1 ~ /^'${date}'./ {print $5,$6,$7,$8}' \
        thermostat_sim_occupant_${occ}.csv \
        > data/may_2013/thermostat_sim_occupant_${occ}_may_${date}.csv
      let date=${date}+1
    done

    while [ ${date} -lt ${JULY_2013} ]
    do
      awk 'BEGIN{ OFS="," ; FS="," } $1 ~ /^'${date}'./ {print $5,$6,$7,$8}' \
        thermostat_sim_occupant_${occ}.csv \
        > data/jun_2013/thermostat_sim_occupant_${occ}_jun_${date}.csv
      let date=${date}+1
    done

done

mv thermostat_sim.csv data/
mv thermostat_sim_occupant_${occ}.csv data/



