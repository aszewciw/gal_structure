#!/bin/bash

cd out_data/
rm *.dat
cd ..

make clean
make

time ./make_galaxy 100000