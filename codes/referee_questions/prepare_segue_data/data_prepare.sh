#!/bin/bash

python pointing_list.py

rm -f ../data/gstar_*.dat

python pickle_gstar_sample.py

python separate_sample.py
