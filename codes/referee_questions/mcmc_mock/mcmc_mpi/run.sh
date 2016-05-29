#! /usr/bin/bash

rm ../data/mcmc_output/mcmc*
make cleanall
make

time mpirun -n 20 ./bin/run_mcmc