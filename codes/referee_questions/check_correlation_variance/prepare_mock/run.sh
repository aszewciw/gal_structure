#! /usr/bin/bash

rm ../data/mock_full*

make cleanall
make

time ./bin/make_galaxy 1000000
python clean_mocks.py

rm ../data/temp*