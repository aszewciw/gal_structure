#!/usr/bin/bash

make cleanall
make

N_procs=20;
N_steps=200000;
filename="../data/mcmc_output/mcmc_result_uniform.dat";

rm $filename

time mpirun -n $N_procs ./bin/run_mcmc -f $filename -N_s $N_steps

# python plot_disk_params.py