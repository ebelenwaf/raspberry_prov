#!/bin/bash

OUTDIR=out

if [[ ! -d ${OUTDIR} ]]; then
  mkdir ${OUTDIR}
fi

for pruning in 0 1 2; do
  OUTDIR=out/${pruning}/
  mkdir ${OUTDIR}
  #for f in 1.0 0.5 0.25 0.125 0.0625 0.03125 0.015625 0.0078125 0.00390625; do
  for f in 1.0 0.0625 0.00390625; do
    mkdir ${OUTDIR}/${f}
    FILE=experiment_data_${f}.txt
    echo -n "" > ${OUTDIR}/${FILE}
    for infile in `ls log/driving_data_*00_* log/driving_data_0_*`; do
      echo "python3 experiment.py -i ${infile} -f ${f} -d 4 -p ${pruning} >> ${OUTDIR}/${FILE}"
      # TODO: Uncomment this when ready to run it for real!
      #python3 experiment.py -i ${infile} -f ${f} -d 4 -p ${pruning} >> ${OUTDIR}/${FILE}
    done
  done
done

