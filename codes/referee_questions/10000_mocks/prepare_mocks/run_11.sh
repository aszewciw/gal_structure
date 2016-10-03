#!/usr/bin/bash

N_stars=1000000;
N_mocks=625;
run_num=11;

time python make_mocks.py $N_stars $N_mocks $run_num