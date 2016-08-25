reset


set xlabel "r_0 (kpc)" font ", 24" offset 0,-1
set ylabel "z_0 (kpc)" font ", 24" offset -1,0
set xtics font ", 18"
set ytics font ", 18"

set xrange[1:5]
set yrange[0.1:1.3]
set cbrange[2000:5000]

set term postscript enhanced color portrait
set size square

set nokey

set output "../plots/mcmc_chain.ps"
plot '../data/mcmc_result.dat' u 2:3:7 w lp pt 7 ps 0.7 lw 2 lc palette, \
     '../data/mcmc_result.dat' u 4:5:7 w lp pt 7 ps 0.7 lw 2 lc palette


set xlabel "z0_{thin} (kpc)" font ", 24" offset 0,-1
set ylabel "z0_{thick} (kpc)" font ", 24" offset -1,0
set xrange[0:0.7]
set yrange[0.6:1.3]

set output "../plots/mcmc_chain_z0.ps"
plot '../data/mcmc_result.dat' u 3:5:9 w lp pt 7 ps 0.7 lw 2 lc palette




#set xlabel "step #" font ", 24" 
#set ylabel "r_0 (kpc)" font ", 24" offset -1,0
#set xrange[0:10000]
#set yrange[2:6]

#set output "r0.vs.steps.ps"
#plot '../data/mcmc.dat' u 1:2 w lp pt 7 ps 0.3 lt 1 lw 1


#set xlabel "step #" font ", 24"
#set ylabel "z_0 (kpc)" font ", 24" offset -1,0
#set xrange[0:10000]
#set yrange[0.1:0.6]

#set output "z0.vs.steps.ps"
#plot '../data/mcmc.dat' u 1:3 w lp pt 7 ps 0.3 lt 1 lw 1




