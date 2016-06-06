#! /usr/bin/bash

rm ./data/*.dat

make cleanall
make

N_stars=10000000;
N_vols=1;

time ./bin/make_galaxy $N_stars $N_vols
