#! /usr/bin/bash

rm ./data/*.dat

make cleanall
make

N_stars=1000000;
star_factor=10;

time ./bin/make_galaxy $N_stars $star_factor
python clean_mocks.py $star_factor

rm ./data/temp*