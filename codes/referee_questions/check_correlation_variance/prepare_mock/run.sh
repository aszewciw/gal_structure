#! /usr/bin/bash

rm ../data/mock_full*

make cleanall
make

Nstars=30000000;

time ./bin/make_galaxy $Nstars
python clean_mocks.py

rm ../data/temp*