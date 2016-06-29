#!/usr/bin/bash

rm ../data/model_pairs/*.dat
rm uni_pair_count

icc -Wall -xHost -O3 -vec_report2 uni_pair_count.c -o uni_pair_count

python uni_pair_count.py