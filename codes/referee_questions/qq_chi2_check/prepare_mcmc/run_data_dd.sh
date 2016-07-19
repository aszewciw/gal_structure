#!/usr/bin/bash

rm ../data/data_dd/*.dat
rm data_pair_count

icc -Wall -xHost -O3 -vec_report2 data_pair_count.c -o data_pair_count

python prepare_segue.py
python data_pair_count.py