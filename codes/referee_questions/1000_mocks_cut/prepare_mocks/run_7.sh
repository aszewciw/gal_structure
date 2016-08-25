#!/usr/bin/bash

N_stars=1000000;
N_mocks=100;
run_num=7;

time python make_mocks.py $N_stars $N_mocks $run_num