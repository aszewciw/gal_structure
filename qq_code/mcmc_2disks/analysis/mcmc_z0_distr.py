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
    
    z0_thin = z0_thin[2000:]
    print_stats(z0_thin)

    plt.figure()
    plt.title(r'Thin Disk Scale Height', fontsize='xx-large')
    plt.xlabel(r'$Z_{0, thin}(kpc)$', fontsize=40)
    plt.ylabel(r'$p(Z_0)$', fontsize=40)
    plt.xticks([0.21,0.23,0.25])
    plt.tick_params(labelsize=40)
    plt.hist(z0_thin, bins=50, range=(0.205, 0.265), 
             normed=True, histtype='step', linewidth=3, color='k')
    plt.text(0.24, 55, r'233$\pm$7 pc', fontweight='bold', fontsize='xx-large')
    plt.tight_layout()
    plt.savefig(config.plots_dir + 'z0_thin_distr.png')
    plt.savefig(config.plots_dir + 'z0_thin_distr.eps')



    z0_thick = z0_thick[2000:]
    print_stats(z0_thick)
    
    plt.figure()
    plt.title(r'Thick Disk Scale Height', fontsize='xx-large')
    plt.xlabel(r'$Z_{0, thick}(kpc)$', fontsize=40)
    plt.ylabel(r'$p(Z_0)$', fontsize=40)
    plt.hist(z0_thick, bins=50, range=(0.6, 0.75),
             normed=True, histtype='step', linewidth=3, color='k')
    plt.xticks([0.62, 0.68, 0.74])
    plt.tick_params(labelsize=40)
    plt.text(0.69, 27.5, r'674$\pm$16 pc', fontweight='bold', fontsize='xx-large')
    plt.tight_layout()
    plt.savefig(config.plots_dir + 'z0_thick_distr.png')
    plt.savefig(config.plots_dir + 'z0_thick_distr.eps')

    plt.figure()
    plt.xlabel(r'$Z_{0}$', fontsize=30)
    plt.ylabel(r'$p(Z_{0})$', fontsize=22)
    plt.hist(z0_thin, bins=50, range=(0.205, 0.265), color='k',
             normed=True, histtype='step', linewidth=3, label=r'$z_{0, thin}$')
    plt.hist(z0_thick, bins=50, range=(0.6, 0.75), color='k',
             normed=True, histtype='step', linewidth=3, label=r'$z_{0, thick}$')
    plt.legend()
    plt.savefig(config.plots_dir + 'z0_distr.eps')

if __name__ == '__main__':
    main()
