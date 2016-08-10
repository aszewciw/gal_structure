#!/usr/bin/bash

rm ../data/mcmc_output/mcmc*
make cleanall
make

N_procs=30;
N_steps=10000;
params=1;
filename=mcmc_result.dat;

rm ../data/mcmc_output/$filename

time mpirun -n $N_procs ./bin/run_mcmc $N_steps $params $filename

python plot_disk_params.py