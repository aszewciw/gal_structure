reset


set xlabel "r_0 (kpc)" font ", 24" offset 0,-1
set ylabel "z_0 (kpc)" font ", 24" offset -1,0
set xtics font ", 18"
set ytics font ", 18"

set xrange[1.5:5.5]
set yrange[0.25:0.65]


set term postscript enhanced color portrait
set size square

set nokey

set output "./plots/mcmc_chain.ps"
plot './data/mcmc.dat' u 2:3:6 w lp pt 7 ps 0.7 lw 2 lc palette



set xlabel "step #" font ", 24" 
set ylabel "r_0 (kpc)" font ", 24" offset -1,0
set xrange[0:1000]
set yrange[2:6]

set output "./plots/r0.vs.steps.ps"
plot './data/mcmc.dat' u 1:2 w lp pt 7 ps 0.3 lt 1 lw 1


set xlabel "step #" font ", 24"
set ylabel "z_0 (kpc)" font ", 24" offset -1,0
set xrange[0:1000]
set yrange[0.3:0.6]

set output "./plots/z0.vs.steps.ps"
plot './data/mcmc.dat' u 1:3 w lp pt 7 ps 0.3 lt 1 lw 1




