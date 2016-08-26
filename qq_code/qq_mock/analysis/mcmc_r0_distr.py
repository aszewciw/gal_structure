#!/usr/bin/env python


import sys, math
import numpy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import config

def print_stats(x):

    sigma_1 = 0.6827

    x = numpy.sort(x)
    x_mean = numpy.mean(x)
    x_median = numpy.median(x)

    n1 = int((1.0 - sigma_1) / 2.0 * len(x))
    n2 = int((1.0 - (1.0 - sigma_1) / 2.0) * len(x))

    err = (x[n2] - x[n1]) / 2.0

    sys.stdout.write('mean = {},  median = {}, err = {} \n'.
                     format(x_mean, x_median, err))

    return x_mean, x_median, err


def main():

    font = {'family' : 'sans-serif',
            'sans-serif' : ['Helvetica'], 
            'size' : 22}

    matplotlib.rc('font', **font)
    matplotlib.rc('text', usetex=True)

    matplotlib.rc('lines', lw=4)

    mcmc_filename = config.data_dir + 'mcmc_result.dat'
    (i, r0_thin, z0_thin, r0_thick, z0_thick, n0_thick,
     chi2, dof, chi2_reduced) = numpy.loadtxt(mcmc_filename, unpack=True)
    
    r0_thin = r0_thin[2000:]
    print_stats(r0_thin)

    plt.figure()
    plt.title(r'Thin Disk Scale Length', fontsize='xx-large')
    plt.xlabel(r'$R_{0, thin}(kpc)$', fontsize=40)
    plt.ylabel(r'$p(R_0)$', fontsize=40)
    plt.xticks([1.5, 2.5, 3.5, 4.5])
    plt.tick_params(labelsize=40)
    plt.hist(r0_thin, bins=50, range=(1.0, 4.5),
             normed=True, histtype='step', linewidth=3, color='k')
    plt.ylim(ymin=0)
    plt.text(2.3, 0.9, r'2.34$\pm$0.48 kpc', fontweight='bold', fontsize='xx-large')
    plt.tight_layout()
    plt.savefig(config.plots_dir + 'r0_thin_distr.png')
    plt.savefig(config.plots_dir + 'r0_thin_distr.eps')

    #hist, bin_edges = numpy.histogram(r0_thin, bins=30, range=(2.0, 2.5), normed=True)
    #print bin_edges, hist

    r0_thick = r0_thick[2000:]
    print_stats(r0_thick)
    
    plt.figure()
    plt.title(r'Thick Disk Scale Length', fontsize='xx-large')
    plt.xlabel(r'$R_{0, thick}(kpc)$', fontsize=40)
    plt.ylabel(r'$p(R_0)$', fontsize=40)
    plt.xticks([2.0, 2.5, 3.0, 3.5])
    plt.tick_params(labelsize=40)
    plt.hist(r0_thick, bins=50, range=(1.6, 3.6),
             normed=True, histtype='step', linewidth=3, color='k')
    plt.ylim(ymin=0)
    plt.text(2.4, 2.25, r'2.51$\pm$0.19 kpc', fontweight='bold', fontsize='xx-large')
    plt.tight_layout()
    plt.savefig(config.plots_dir + 'r0_thick_distr.png')
    plt.savefig(config.plots_dir + 'r0_thick_distr.eps')

if __name__ == '__main__':
    main()
