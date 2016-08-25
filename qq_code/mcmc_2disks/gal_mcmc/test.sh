#!/bin/bash


#gcc -Wall -lm -lgsl -lgslcblas -g -O0 main.c io.c model.c functions.c correlation.c mcmc.c -o test
#valgrind --leak-check=yes test


#gcc -Wall -lm -lgsl -lgslcblas -g -pg -O0 main.c io.c model.c functions.c correlation.c mcmc.c -o test
#./test
#gprof test gmon.out > tmplog


gcc -Wall -lm -lgsl -lgslcblas -O3 main.c io.c model.c functions.c correlation.c mcmc.c -o test
#./test  > tmplog 2>&1
#./test


gcc -Wall -lm -lgsl -lgslcblas -O3 test_correlation.c io.c model.c functions.c correlation.c mcmc.c -o test_correlation

gcc -Wall -lm -lgsl -lgslcblas -O3 test_chi2.c io.c model.c functions.c correlation.c mcmc.c -o test_chi2



