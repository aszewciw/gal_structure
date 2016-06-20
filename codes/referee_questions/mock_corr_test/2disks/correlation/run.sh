#! /usr/bin/bash

rm ../data/*.xyzw.dat
rm ../data/stat_data.dat
rm correlation

# prepare uniforms
python rand_to_model.py

# prepare mocks
python xyz_to_xyzw.py

# run correlation
gcc -Wall -O3 correlation.c -o correlation
python correlation.py

# run statistics
python average.py