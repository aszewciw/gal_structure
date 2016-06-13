#!/usr/bin/bash

rm ../data/rbins/*.dat
python set_rbins.py

rm ../data/jackknife/uniform*
rm counts

icc -Wall -xHost -O3 -vec_report2 counts.c -o counts

python prepare_uniform_jackknife.py
time python uniform_error_jk.py