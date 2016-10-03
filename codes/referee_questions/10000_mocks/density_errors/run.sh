#!/usr/bin/bash

rm -r ./data/*.dat

Nbins=5;
Nmocks=1000;

python choose_r_values.py $Nbins

python normalized_mock_density.py $Nmocks