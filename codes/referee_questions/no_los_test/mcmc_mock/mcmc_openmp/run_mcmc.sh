#!/usr/bin/bash

rm ../data/mcmc_output/mcmc*
make cleanall
make

N_threads=16;
N_steps=1;

export OMP_NUM_THREADS=$N_threads

time mpirun -n $N_procs ./bin/run_mcmc $N_steps