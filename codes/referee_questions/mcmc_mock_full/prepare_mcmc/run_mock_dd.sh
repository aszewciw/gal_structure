#!/usr/bin/bash

rm ../data/mock_dd/*.dat
rm mock_pair_count

icc -Wall -xHost -O3 -vec_report2 mock_pair_count.c -o mock_pair_count

python mock_pair_count.py