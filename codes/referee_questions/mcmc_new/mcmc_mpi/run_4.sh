#!/usr/bin/bash

make cleanall
make

N_procs=20;
filename="../data/mcmc_output/mcmc_result_4.dat";
r0_thin=1.5;
z0_thin=1.0;
r0_thick=1.5;
z0_thick=2.0;
ratio=0.2;


rm $filename

time mpirun -n $N_procs ./bin/run_mcmc -f $filename -rn $r0_thin -zn $z0_thin -rk $r0_thick -zk $z0_thick -a $ratio
# python plot_disk_params.py