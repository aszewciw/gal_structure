#!/bin/bash

make gal_mcmc

export OMP_NUM_THREADS=8
time ./gal_mcmc
