#!/usr/bin/bash

# rm ../data/mcmc_output/mcmc*
make cleanall
make

N_procs=12;
N_steps=0;
r0_thin=2.2;
z0_thin=0.25;
r0_thick=2.3;
z0_thick=0.6;
ratio=0.15;

time mpirun -n $N_procs ./bin/run_mcmc -N_s $N_steps -rn $r0_thin -zn $z0_thin -rk $r0_thick -zk $z0_thick -a $ratio