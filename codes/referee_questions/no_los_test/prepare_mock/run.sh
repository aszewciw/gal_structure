#! /usr/bin/bash

rm ./data/*.dat

make cleanall
make

# same number of stars as are in data
N_stars=18067;

time ./bin/make_galaxy 1000000

rm ./data/temp*