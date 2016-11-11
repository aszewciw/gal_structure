#!/usr/bin/bash

cp ../../mcmc_A/data/rbins/*.dat ../data/rbins/

bash run_mock_dd.sh

bash run_pair_binning.sh

rm ../data/model_positions/*.dat
rm ../data/errors/*.dat
rm ../../data/pointing_ID.dat
python clean_data.py