#! /usr/bin/bash

rm mock_pair_count
icc -Wall -xHost -O3 -vec_report2 mock_pair_count.c -o mock_pair_count

N_mocks=2;
time python mock_pair_count.py $N_mocks

rm -rf ../data/mean_var_std/
mkdir ../data/mean_var_std
python average.py $N_mocks