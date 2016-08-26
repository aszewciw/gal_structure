#!/bin/bash

make

export OMP_NUM_THREADS=16
time ./gal_mcmc