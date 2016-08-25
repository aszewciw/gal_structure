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
    
    n0_thick = n0_thick[2000:]
    print_stats(n0_thick)

    plt.figure()
    plt.title(r'$n_{0, thick} / n_{0, thin}$')
    plt.xlabel(r'$n_{0, thick} / n_{0, thin}$', fontsize=30)
    plt.ylabel(r'$p(r)$', fontsize=22)
    plt.hist(n0_thick, bins=50, range=(0, 0.3),
             normed=True, histtype='step', linewidth=3)
    plt.ylim(ymin=0)
    plt.tight_layout()
    #plt.text(0.243, 48, r'$\pm$ kpc', fontweight='bold', fontsize='x-large')
    plt.savefig(config.plots_dir + 'n0_thick_distr.png')


if __name__ == '__main__':
    main()
