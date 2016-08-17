#! /usr/bin/bash

rm ./data/*.dat

make cleanall
make

nprocs=32;
nstars=10000000;

time mpirun -n $nprocs ./bin/make_galaxy $nstars
python clean_mocks.py $nprocs

# rm ./data/proc*