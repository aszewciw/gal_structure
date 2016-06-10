#! /usr/bin/bash

rm -rf ../data/mock_dd
rm mock_pair_count

mkdir ../data/mock_dd

icc -Wall -xHost -O3 -vec_report2 mock_pair_count.c -o mock_pair_count

python mock_pair_count.py