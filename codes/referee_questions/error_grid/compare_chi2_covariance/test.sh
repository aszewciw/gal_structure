#! /usr/bin/bash

plt='test';
N=12;
mock=$1;
lines='ttt tte ttf tft tfe tff ett ete etf eft efe eff'
python gif_compare_chi2.py $N $mock $plt $lines