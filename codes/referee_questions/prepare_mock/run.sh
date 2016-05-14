#!/bin/bash

rm data/*.dat

make cleanall
make

time ./bin/make_galaxy 1000000