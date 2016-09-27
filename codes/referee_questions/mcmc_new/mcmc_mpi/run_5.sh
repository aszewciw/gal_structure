#!/usr/bin/bash

make cleanall
make

N_procs=20;
filename="../data/mcmc_output/mcmc_result_5.dat";
r0_thin=4.0;
z0_thin=3.0;
r0_thick=3.0;
z0_thick=5.0;
ratio=0.1;


rm $filename

time mpirun -n $N_procs ./bin/run_mcmc -f $filename -rn $r0_thin -zn $z0_thin -rk $r0_thick -zk $z0_thick -a $ratio
# python plot_disk_params.py