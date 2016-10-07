#!/usr/bin/bash

rm ./plots/*.gif
rm ./plots/*.png

python mm_compare_gif.py 1000
python mm_compare_gif.py 10000