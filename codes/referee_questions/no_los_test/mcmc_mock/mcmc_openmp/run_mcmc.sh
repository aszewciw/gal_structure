#!/usr/bin/bash

rm ../data/mcmc_output/mcmc*
make cleanall
make

N_threads=32;
N_steps=200;

export OMP_NUM_THREADS=$N_threads

time ./bin/run_mcmc $N_steps