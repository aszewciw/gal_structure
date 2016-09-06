#!/usr/bin/bash

make cleanall
make

N_procs=20;

rm ../data/mcmc_output/$filename

time mpirun -n $N_procs ./bin/run_mcmc

python plot_disk_params.py