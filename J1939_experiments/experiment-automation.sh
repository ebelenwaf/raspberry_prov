#!/bin/bash

OUTDIR=out

if [[ ! -d ${OUTDIR} ]]; then
  mkdir ${OUTDIR}
fi

#if [[ -f ${OUTDIR}/${FILE} ]]; then
#  echo "remove previous sim_res.txt"
#  exit 1
#fi
#touch ${OUTDIR}/${FILE}

## Variables are:
##  tasks
##  utilization (and distribution)
##  pq size (min/max)
##  pq ops (min/max)

## FIXME: use more trials
#TRIALS=100000
TRIALS=10000

## FIXME: vary the util distribution
#for dist in 1 2 3


  for pruning in 0 1 2; do
    OUTDIR=out/${pruning}/
    mkdir ${OUTPUT}
    for f in 1.0 0.5 0.25 0.125; do
      FILE=experiment_data_${f}.txt
      for x in {0..2}; do
        python experiment.py -i log/anomalous_data_${0}.csv -f ${f} -d 4 ... >> ${OUTDIR}/${FILE}

      done
    done
  done

