#!/usr/bin/bash

make cleanall
make

N_procs=28;
N_steps=200000;
params=1;
filename=mcmc_result_4.dat;

rm ../data/mcmc_output/$filename

time mpirun -n $N_procs ./bin/run_mcmc $N_steps $params $filename

# python plot_disk_params.py