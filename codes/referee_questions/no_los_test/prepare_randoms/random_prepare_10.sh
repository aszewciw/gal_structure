#!/usr/bin/bash

rm ./data/uniform*

N_data=18067;
factor=10;

time python generate_randoms.py $N_data $factor