#!/bin/bash

rm ../data/mcmc_output/mcmc*
# make cleanall
# make

time mpirun -n 1 ./bin/run_mcmc