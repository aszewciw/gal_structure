#!/usr/bin/bash

N_procs=$1

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

N_stars=1000000;
N_mocks=1000;

time python make_mocks.py $N_stars $N_mocks $N_procs
python check_files.py