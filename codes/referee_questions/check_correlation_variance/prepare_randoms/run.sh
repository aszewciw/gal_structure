#!/usr/bin/bash

rm ../data/uniform*

python gen_rand_10data.py
python gen_rand_10mock.py
python gen_rand_1500.py
python gen_rand_2000.py
