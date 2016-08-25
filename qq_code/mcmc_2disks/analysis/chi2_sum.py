#!/usr/bin/env python

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


input_filename = '../data/chi2_los.dat'
pid, chi2_los = np.loadtxt(input_filename, unpack=True)

print sum(chi2_los)
