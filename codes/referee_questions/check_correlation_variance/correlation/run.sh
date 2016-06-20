#!/usr/bin/bash

rm ../data/corr_full*
rm correlation

icc -Wall -xHost -O3 -vec_report2 correlation.c -o correlation


type1=10data;
type2=10mock;
type3=1500;
type4=2000;

python correlation_full.py $type1
python correlation_full.py $type2
python correlation_full.py $type3
python correlation_full.py $type4