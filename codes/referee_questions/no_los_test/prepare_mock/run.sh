#!/usr/bin/bash

rm ./data/*.dat

make cleanall
make

# same number of stars as are in data
# N_stars=18067;
N_stars=30000;

time ./bin/make_galaxy $N_stars