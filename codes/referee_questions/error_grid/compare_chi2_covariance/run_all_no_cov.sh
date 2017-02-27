#! /usr/bin/bash

plt='all_no_cov';
N=6;
mock=$1;
lines='tnt tne tnf ent ene enf'
# python gif_compare_chi2.py $N $mock $plt $lines
python compare_chi2_ninepanels.py $N $mock $plt $lines