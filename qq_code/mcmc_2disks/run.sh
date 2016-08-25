#!/bin/bash

cd data_prepare
sh data_prepare.sh
cd ..

cd calculate_error
sh run.sh
cd ..


