#!/usr/bin/env python

import sys, math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import config

def print_stats(x):

    sigma_1 = 0.6827

    x = np.sort(x)
    x_mean = np.mean(x)
    x_median = np.median(x)

    n1 = int((1.0 - sigma_1) / 2.0 * len(x))
    n2 = int((1.0 - (1.0 - sigma_1) / 2.0) * len(x))

    err = (x[n2] - x[n1]) / 2.0

    sys.stdout.write('mean = {},  median = {}, err = {} \n'.
                     format(x_mean, x_median, err))

    return x_mean, x_median, err


font = {'family' : 'sans-serif',
        'sans-serif' : ['Helvetica'], 
        'size' : 22}

matplotlib.rc('font', **font)
matplotlib.rc('text', usetex=True)

matplotlib.rc('lines', lw=4)

mcmc_filename = config.data_dir + 'mcmc_result.dat'
(i, r0_thin, z0_thin, r0_thick, z0_thick, n0_thick,
 chi2, dof, chi2_reduced) = np.loadtxt(mcmc_filename, unpack=True)
    
z0_thin = z0_thin[2000:]
print_stats(z0_thin)

# plt.figure()
# plt.title(r'Thin Disk Scale Height')
# plt.xlabel(r'$z_{0, thin}$', fontsize=30)
# plt.ylabel(r'$p(z)$', fontsize=22)
# plt.hist(z0_thin, bins=50, range=(0.205, 0.265),
#          normed=True, histtype='step', linewidth=3)
# plt.text(0.243, 48, r'233$\pm$7 pc', fontweight='bold', fontsize='x-large')
# plt.savefig(config.plots_dir + 'z0_thin_distr.png')



# z0_thick = z0_thick[2000:]
# print_stats(z0_thick)

# plt.figure()
# plt.title(r'Thick Disk Scale Height')
# plt.xlabel(r'$z_{0, thick}$', fontsize=30)
# plt.ylabel(r'$p(z)$', fontsize=22)
# plt.hist(z0_thick, bins=50, range=(0.6, 0.75),
#          normed=True, histtype='step', linewidth=3)
# plt.text(0.7, 24, r'674$\pm$16 pc', fontweight='bold', fontsize='x-large')
# plt.savefig(config.plots_dir + 'z0_thick_distr.png')

