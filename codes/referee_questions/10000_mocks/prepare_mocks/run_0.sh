#!/bin/bash

N_stars=1000000;
N_mocks=625;
# run_num=0;

# time python make_mocks.py $N_stars $N_mocks $run_num




Windows_names="Run_SSh"
screen -mdS ${Windows_names}
for i in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
do
    screen -S ${Windows_names} -X screen -t ${i}
    screen -S ${Windows_names} -p ${i} -X stuff "python make_mocks.py $N_stars $N_mocks $i"
    screen -S ${Windows_names} -p ${i} -X stuff "\n"
done