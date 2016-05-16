#!/bin/bash

rm ./data/mcmc*

time mpirun -n 32 ./bin/run_mcmc