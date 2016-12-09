#!/usr/bin/bash

make cleanall
make

N_procs=20;
steps=500000;
filename="../data/mcmc_output/mcmc_result.dat";

rm $filename

time mpirun -n $N_procs ./bin/run_mcmc -f $filename -N_s $steps

# python plot_disk_params.py