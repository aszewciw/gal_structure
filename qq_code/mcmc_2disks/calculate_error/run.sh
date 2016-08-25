#!/bin/bash



gcc -Wall -O3 -lm -o counts counts.c


python error.py
python error_uniform.py