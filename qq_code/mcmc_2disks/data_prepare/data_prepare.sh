#!/bin/bash

# use the todo list from the data
cp /fs1/mqq/Projects/StarClustering/segue/correlation/data/todo_list.dat ../data/
python convert_todo_list.py

# set the bins, these bin settings will be used for correlation function calculations
python set_bins.py

# prepare data
python prepare_data.py
python prepare_data_jackknife.py


# generate uniform
python prepare_uniform.py
python prepare_uniform_jackknife.py
