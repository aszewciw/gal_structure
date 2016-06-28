#!/usr/bin/bash

#remove directories
rm -rf ./data/mock*

# make directories
n=1;
N_mocks=1000;
while [ "$n" -le "$N_mocks" ]; do
    mkdir "./data/mock_$n"
    n=`expr "$n" + 1`;
done

make cleanall
make

N_stars=30000000;
N_mocks=1000;
run_num=0;

time python make_mocks.py $N_stars $N_mocks $run_num