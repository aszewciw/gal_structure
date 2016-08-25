#!/usr/bin/env python

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


input_filename = '../data/chi2_los.dat'
pid, chi2_los = np.loadtxt(input_filename, unpack=True)

input_filename = '../../mcmc_kelly_newparams_2disks/data/chi2_los.dat'
pid_model, chi2_los_model = np.loadtxt(input_filename, unpack=True)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel(r'$\chi ^2$')
ax.set_ylabel(r'$n(\chi)$')

ax.hist(chi2_los, bins=30, histtype='step', normed=True, label='data')
ax.hist(chi2_los_model, bins=30, histtype='step', normed=True, label='model')

ax.legend()

fig.savefig('../plots/chi2_los.png')
