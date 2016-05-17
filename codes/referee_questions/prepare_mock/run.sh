#!/bin/bash

rm ./data/mock*
rm ./data/temp*

make cleanall
make

time ./bin/make_galaxy 10000000
python clean_mocks.py

rm ./data/temp*