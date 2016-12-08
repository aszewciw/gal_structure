#! /usr/bin/bash

plt='all_cov';
N=6;
mock=$1;
lines='tnt tne tnf ent ene enf'
python gif_compare_chi2.py $N $mock $plt $lines