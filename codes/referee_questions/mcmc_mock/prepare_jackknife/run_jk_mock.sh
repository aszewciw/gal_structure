#! /usr/bin/bash

rm ../data/jacknife/mock*
rm counts

icc -Wall -xHost -O3 -vec_report2 counts.c -o counts

python prepare_mock_jackknife.py
python mock_error_jk.py