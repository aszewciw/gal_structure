#!/usr/bin/bash

rm ../data/rbins/*.dat
python set_rbins.py

rm ../data/jackknife/mock*
rm ../data/jackknife/uniform*
rm counts

icc -Wall -xHost -O3 -vec_report2 counts.c -o counts

python prepare_mock_jackknife.py
python mock_error_jk.py

python prepare_uniform_jackknife.py
python uniform_error_jk.py