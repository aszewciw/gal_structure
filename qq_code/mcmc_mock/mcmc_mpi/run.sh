#!/usr/bin/bash

make cleanall
make

N_procs=20;
N_steps=500000;
params=0;
filename=mcmc_result.dat;

rm ../data/mcmc_output/$filename

time mpirun -n $N_procs ./bin/run_mcmc $N_steps $params $filename

# python plot_disk_params.py