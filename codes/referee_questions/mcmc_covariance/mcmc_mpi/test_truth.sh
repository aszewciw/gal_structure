#!/usr/bin/bash

# rm ../data/mcmc_output/mcmc*
make cleanall
make

N_procs=20;
N_steps=0;
params=0;
filename=mcmc_result.dat;

time mpirun -n $N_procs ./bin/run_mcmc $N_steps $params $filename
