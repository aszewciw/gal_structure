#!/usr/bin/bash

rm ./data/uniform*

N_data=18067;
factor=3;

time python generate_randoms.py $N_data $factor