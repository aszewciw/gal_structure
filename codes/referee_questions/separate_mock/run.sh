#!/bin/bash

rm ../data/mock*

make cleanall
make

time ./separate_gal