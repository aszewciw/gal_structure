#!/usr/bin/bash

rm ../data/mcmc_output/mcmc*
make cleanall
make

N_threads=16;
N_steps=10000;

export OMP_NUM_THREADS=$N_threads

time ./bin/run_mcmc $N_steps