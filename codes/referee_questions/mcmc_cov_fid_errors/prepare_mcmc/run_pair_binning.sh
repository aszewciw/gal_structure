#! /usr/bin/bash

rm ../data/model_pairs/*.dat
rm nonuni_pair_count

icc -Wall -xHost -O3 -vec_report2 nonuni_pair_count.c -o nonuni_pair_count

python nonuni_pair_count.py