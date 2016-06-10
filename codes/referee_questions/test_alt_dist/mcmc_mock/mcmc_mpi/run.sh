#!/usr/bin/bash

rm ../data/mcmc_output/mcmc*
make cleanall
make

N_procs=20;
N_steps=400000;

time mpirun -n $N_procs ./bin/run_mcmc $N_steps