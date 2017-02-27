#! /usr/bin/bash

plt='bstar_gsquare';
N=4;
mock=$1;
lines='ttt ett tff eff'
# python gif_compare_chi2.py $N $mock $plt $lines
python compare_chi2_ninepanels.py $N $mock $plt $lines