#!/bin/bash

make test_chi2

export OMP_NUM_THREADS=8
time ./test_chi2
