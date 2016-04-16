#!/bin/bash

make test_correlation

export OMP_NUM_THREADS=8
time ./test_correlation
