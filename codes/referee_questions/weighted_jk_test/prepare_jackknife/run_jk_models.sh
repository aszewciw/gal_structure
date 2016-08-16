#!/usr/bin/bash

# rm ../data/rbins/*.dat
python set_rbins.py

# rm ../data/jackknife/uniform*
rm counts

icc -Wall -xHost -O3 -vec_report2 counts.c -o counts

python prepare_uniform_jackknife.py 0
python uniform_error_jk.py 0

python prepare_uniform_jackknife.py 1
python uniform_error_jk.py 1