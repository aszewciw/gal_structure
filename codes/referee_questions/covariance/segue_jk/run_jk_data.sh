#!/usr/bin/bash

rm ../data/*rbins
python set_rbins.py

rm ../data/jackknife/star*
rm counts

icc -Wall -xHost -O3 -vec_report2 counts.c -o counts

python prepare_data_jackknife.py
python data_error_jk.py