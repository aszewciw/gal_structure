#! /usr/bin/bash

plt='all_combos';
N=18;
mock=$1;
lines='ttt tte ttf tft tfe tff tnt tne tnf ett ete etf eft efe eff ent ene enf'
python gif_compare_chi2.py $N $mock $plt $lines