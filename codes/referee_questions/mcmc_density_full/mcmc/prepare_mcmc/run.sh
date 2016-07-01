#!/usr/bin/bash

rm ../data/rbins/*.dat
rm ../data/model_positions/*.dat
rm ../data/mock_density/*.dat
rm ../data/mock_errors/*.dat

N_bins=5;

python choose_r_values.py $N_bins
python separate_randoms.py
python normalized_mock_density.py
python errors.py