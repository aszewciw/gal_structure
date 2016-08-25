#!/bin/bash

# use the todo list from the data
cp /fs1/mqq/Projects/StarClustering/segue/correlation/data/todo_list.dat ../data/
python convert_todo_list.py

# set the bins, these bin settings will be used for correlation function calculations
./set_bins.py

# prepare data
./prepare_data.py
./prepare_data_jackknife.py


# generate uniform
./prepare_uniform.py
./prepare_uniform_jackknife.py
