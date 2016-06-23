#!/usr/bin/bash

rm ../data/mcmc_output/mcmc*
make cleanall
make

N_steps=1;
N_procs=8;

time mpirun -n $N_procs ./bin/run_mcmc $N_steps