#!/usr/bin/bash

rm ../data/mcmc_output/mcmc*
make cleanall
make

N_procs=12;
N_steps=10;

time mpirun -n $N_procs ./bin/run_mcmc $N_steps