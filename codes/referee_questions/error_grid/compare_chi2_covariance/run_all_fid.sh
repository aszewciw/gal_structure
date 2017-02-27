#! /usr/bin/bash

plt='all_fid';
N=4;
mock=$1;
lines='tff eff tnf enf';
# python gif_compare_chi2.py $N $mock $plt $lines
python compare_chi2_ninepanels.py $N $mock $plt $lines