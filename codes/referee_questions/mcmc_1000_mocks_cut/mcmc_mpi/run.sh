#!/usr/bin/bash

rm ../data/mcmc_output/mcmc*
make cleanall
make

N_procs=30;
N_steps=300000;
params=1;

time mpirun -n $N_procs ./bin/run_mcmc $N_steps $params