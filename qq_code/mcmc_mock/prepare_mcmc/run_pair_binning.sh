#! /usr/bin/bash

rm ../data/model_pairs/*.dat
rm ../data/uniform/*.xyz.dat
python ascii_to_xyz.py
rm uni_pair_count

icc -Wall -xHost -O3 -vec_report2 uni_pair_count.c -o uni_pair_count

python uni_pair_count.py