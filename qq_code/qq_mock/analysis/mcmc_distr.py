#!/usr/bin/env python


import sys, math
import numpy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import config

font = {'family' : 'sans-serif',
        'sans-serif' : ['Helvetica'], 
        'size' : 22}

matplotlib.rc('font', **font)
matplotlib.rc('text', usetex=True)

matplotlib.rc('lines', lw=4)

mcmc_filename = config.data_dir + 'mcmc_result.dat'
(i, r0_thin, z0_thin, r0_thick, z0_thick, n0_thick,
 chi2, dof, chi2_reduced) = numpy.loadtxt(mcmc_filename, unpack=True)

plt.figure()
plt.xlabel(r'$i$')
plt.ylabel(r'$r_{0, thin}$')
plt.plot(i, r0_thin)
plt.savefig(config.plots_dir + 'r0_thin.png')

plt.figure()
plt.xlabel(r'$i$')
plt.ylabel(r'$z_{0, thin}$')
plt.plot(i, z0_thin)
plt.savefig(config.plots_dir + 'z0_thin.png')

plt.figure()
plt.xlabel(r'$i$')
plt.ylabel(r'$r_{0, thick}$')
plt.plot(i, r0_thick)
plt.savefig(config.plots_dir + 'r0_thick.png')

plt.figure()
plt.xlabel(r'$i$')
plt.ylabel(r'$z_{0, thick}$')
plt.plot(i, z0_thick)
plt.savefig(config.plots_dir + 'z0_thick.png')

plt.figure()
plt.xlabel(r'$i$')
plt.ylabel(r'$\frac{n_{0, thick}}{n_{0, thin}}$')
plt.plot(i, n0_thick)
plt.savefig(config.plots_dir + 'n0_thick.png')



plt.figure()
plt.title(r'Thin Disk Scale Height')
plt.xlabel(r'$z_{0, thin}$', fontsize=30)
plt.ylabel(r'$p(z)$', fontsize=22)
plt.hist(z0_thin[2000:], bins=50, range=(0.205, 0.265),
         normed=True, histtype='step', linewidth=3)
plt.savefig(config.plots_dir + 'z0_thin_distr.png')

plt.figure()
plt.title(r'Thick Disk Scale Height')
plt.xlabel(r'$z_{0, thick}$', fontsize=30)
plt.ylabel(r'$p(z)$', fontsize=22)
plt.hist(z0_thick[2000:], bins=50, range=(0.6, 0.75),
         normed=True, histtype='step', linewidth=3)
plt.savefig(config.plots_dir + 'z0_thick_distr.png')

plt.figure()
plt.title(r'Thin Disk Scale Length')
plt.xlabel(r'$r_{0, thin}$')
plt.ylabel(r'$p(r)$')
plt.hist(r0_thin[2000:], bins=30, range=(2.0, 2.6),
         normed=True, histtype='step', linewidth=3)
plt.savefig(config.plots_dir + 'r0_thin_distr.png')

plt.figure()
plt.title(r'Thick Disk Scale Length')
plt.xlabel(r'$r_{0, thick}$')
plt.ylabel(r'$p(r)$')
plt.hist(r0_thick[2000:], bins=30, range=(2.3, 2.7),
         normed=True, histtype='step', linewidth=3)
plt.savefig(config.plots_dir + 'r0_thick_distr.png')

plt.figure()
plt.title(r'$n_{0, thick} / n_{0, thin}$')
plt.xlabel(r'$\frac{n_{0, thick}}{n_{0, thin}}$')
plt.ylabel(r'$p$')
plt.hist(n0_thick[2000:], bins=100, range=(0, 0.3),
         normed=True, histtype='step', linewidth=3)
plt.savefig(config.plots_dir + 'n0_thick_distr.png')
