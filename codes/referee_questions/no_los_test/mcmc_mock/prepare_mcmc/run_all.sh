#!/usr/bin/bash

bash run_mock_dd.sh

bash run_pair_binning.sh

rm ../data/errors/*.dat
python clean_data.py