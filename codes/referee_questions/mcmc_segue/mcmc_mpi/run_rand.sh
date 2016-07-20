#!/usr/bin/bash

rm ../data/mcmc_output/mcmc*
make cleanall
make

N_procs=24;
N_steps=300000;
params=2;

time mpirun -n $N_procs ./bin/run_mcmc $N_steps $params