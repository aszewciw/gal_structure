#! /usr/bin/bash

rm ../data/jackknife/uniform*
rm counts

icc -Wall -xHost -O3 -vec_report2 counts.c -o counts

python uniform_error_jk.py