#!/bin/bash

# make directories
n=1;
N_mocks=10;
while [ "$n" -le "$N_mocks" ]; do
    mkdir "../data/mock_$n"
    n=`expr "$n" + 1`;
done

make cleanall
make


N_stars=1000000;
# time ./bin/make_galaxy 1000000
# python clean_mocks.py

# rm ./data/temp*

python make_mocks.py "$N_stars $N_mocks"