#!/usr/bin/bash
rm ./data/*.dat
make cleanall
make

n=1;
N_mocks=100;
while [ "$n" -le "$N_mocks" ]; do
    bash run.sh
    n=`expr "$n" + 1`;
done