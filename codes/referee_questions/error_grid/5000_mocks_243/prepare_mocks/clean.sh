#!/usr/bin/bash

#remove directories
rm -rf ./data/mock*
cp /fs1/szewciw/gal_structure/codes/referee_questions/data/todo_* ./data/

# make directories
n=1;
N_mocks=5000;
while [ "$n" -le "$N_mocks" ]; do
    mkdir "./data/mock_$n"
    n=`expr "$n" + 1`;
done

make cleanall
make