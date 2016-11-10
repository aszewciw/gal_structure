#!/usr/bin/bash

make cleanall
make

N_procs=20;
filename="../data/mcmc_output/mcmc_result_2.dat";
r0_thin=2.0;
z0_thin=0.2;
r0_thick=5.0;
z0_thick=0.5;
ratio=0.3;


rm $filename

time mpirun -n $N_procs ./bin/run_mcmc -f $filename -rn $r0_thin -zn $z0_thin -rk $r0_thick -zk $z0_thick -a $ratio
# python plot_disk_params.py