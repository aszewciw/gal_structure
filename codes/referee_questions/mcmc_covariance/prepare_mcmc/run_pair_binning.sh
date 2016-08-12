#! /usr/bin/bash

rm ../data/model_pairs/*.dat
rm model_pair_count

icc -Wall -xHost -O3 -vec_report2 model_pair_count.c -o model_pair_count

python model_pair_count.py