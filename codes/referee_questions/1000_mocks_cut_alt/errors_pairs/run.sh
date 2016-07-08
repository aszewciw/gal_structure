#!/usr/bin/bash

# remove directories
rm -rf ./data/mock*

# make directories
n=1;
N_mocks=1000;
while [ "$n" -le "$N_mocks" ]; do
    mkdir "./data/mock_$n"
    n=`expr "$n" + 1`;
done

rm mock_pair_count
icc -Wall -xHost -O3 -vec_report2 mock_pair_count.c -o mock_pair_count

time python mock_pair_count.py $N_mocks

rm -rf ./data/mean_var_std
mkdir ./data/mean_var_std
time python average.py $N_mocks