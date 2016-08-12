#!/usr/bin/bash

rm ../data/uniform_rr/*.dat
rm uniform_pair_count

python set_rbins.py

icc -Wall -xHost -O3 -vec_report2 uniform_pair_count.c -o uniform_pair_count

python uniform_pair_count.py