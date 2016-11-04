#!/usr/bin/bash

# rm ./data/*.dat
rm pair_count

cp /fs1/szewciw/gal_structure/codes/referee_questions/mcmc_mock/data/rbins/*.dat ./data/

icc -Wall -xHost -O3 -vec_report2 pair_count.c -o pair_count

time python pair_count.py 10
time python pair_count.py 50
# time python pair_count.py 100
# time python pair_count.py 1000