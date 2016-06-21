#!/usr/bin/bash

rm ../data/rbins/*.dat
rm ../data/model_positions/*.dat

N_bins=5;

python choose_r_values.py $N_bins
python separate_randoms.py