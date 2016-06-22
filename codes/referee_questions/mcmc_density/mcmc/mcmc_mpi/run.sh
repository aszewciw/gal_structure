#!/usr/bin/bash

rm ../data/mcmc_output/mcmc*
make cleanall
make

N_steps=400000;

time ./bin/run_mcmc $N_steps