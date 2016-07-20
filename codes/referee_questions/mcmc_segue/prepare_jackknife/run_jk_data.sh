#!/usr/bin/bash

rm ../data/rbins/*.dat
python set_rbins.py

rm ../../prepare_segue_data/data/*xyz.dat

rm ../data/jackknife/star*
rm counts

icc -Wall -xHost -O3 -vec_report2 counts.c -o counts

python data_xyzw_to_xyz.py
python prepare_data_jackknife.py
python data_error_jk.py