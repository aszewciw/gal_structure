#! /usr/bin/bash

rm ./data/*.dat

nprocs=19;
nstars=1000000;

time mpirun -n $nprocs ./bin/make_galaxy $nstars
python clean_mocks.py $nprocs

rm ./data/proc*