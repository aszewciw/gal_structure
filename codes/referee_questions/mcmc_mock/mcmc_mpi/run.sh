#!/usr/bin/bash

make cleanall
make

N_procs=20;
# filename="../data/mcmc_output/mcmc_test.dat";

rm $filename

time mpirun -n $N_procs ./bin/run_mcmc -f $filename

# python plot_disk_params.py