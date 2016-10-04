#!/usr/bin/bash

rm ./data/mm*
rm pair_count

icc -Wall -xHost -O3 -vec_report2 pair_count.c -o pair_count

python pair_count.py