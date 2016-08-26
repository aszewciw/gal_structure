#!/bin/bash

# use the todo list from the data
cp /fs1/mqq/Projects/StarClustering/segue/correlation/data/todo_list.dat ../data/todo/
python convert_todo_list.py

python set_rbins.py

python prepare_mock_jackknife.py

python prepare_uniform.py
python prepare_uniform_jackknife.py

gcc -Wall -O3 -lm -o counts counts.c

python error.py
python error_uniform.py