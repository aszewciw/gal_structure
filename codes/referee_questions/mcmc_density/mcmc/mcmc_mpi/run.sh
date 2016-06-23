#!/usr/bin/bash

rm ../data/mcmc_output/mcmc*
make cleanall
make

N_steps=10000;
N_procs=16;

time mpirun -n $N_procs ./bin/run_mcmc $N_steps