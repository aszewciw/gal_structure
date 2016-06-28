#! /usr/bin/bash

rm ./data/*.dat

make cleanall
make

Nstars=30000000;

time ./bin/make_galaxy $Nstars
python clean_mocks.py

rm ./data/temp*