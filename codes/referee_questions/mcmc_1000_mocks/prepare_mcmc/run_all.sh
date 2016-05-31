#!/usr/bin/bash

bash run_mock_dd.sh

bash run_pair_binning.sh

rm ../data/model_positions/*.dat
rm ../data/errors/*.dat
python clean_data.py