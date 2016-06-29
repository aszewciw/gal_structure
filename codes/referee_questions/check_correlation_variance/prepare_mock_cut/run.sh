#!/usr/bin/bash

rm ../data/mock_cut*

make cleanall
make

time ./bin/make_galaxy 1000000
python clean_mocks.py

rm ../data/temp*