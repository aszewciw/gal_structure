#! /usr/bin/bash

plt='all_cov';
N=12;
mock=$1;
lines='tnt tne tnf ent ene enf'
python gif_compare_chi2.py $N $mock $plt $lines