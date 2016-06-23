#!/usr/bin/bash

#remove directories
rm -rf ./data/mock*

# make directories
n=0;
N_mocks=999;
while [ "$n" -le "$N_mocks" ]; do
    mkdir "./data/mock_$n"
    n=`expr "$n" + 1`;
done

make cleanall
make