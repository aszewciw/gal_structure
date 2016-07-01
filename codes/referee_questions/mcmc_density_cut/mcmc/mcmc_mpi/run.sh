#!/usr/bin/bash

rm ../data/mcmc_output/mcmc*
make cleanall
make

N_steps=300000;
N_procs=16;
N_stars=30000000;

time mpirun -n $N_procs ./bin/run_mcmc $N_steps $N_stars