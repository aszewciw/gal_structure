#!/bin/bash

rm ../data/mock*

make cleanall
make

time ./bin/make_galaxy 10000000