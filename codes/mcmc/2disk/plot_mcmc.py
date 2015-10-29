import numpy as np
from config import *
import matplotlib.pyplot as plt

filename = mcmcdata_dir + 'testdata.npz'


with np.load(filename) as d:
    a         = d['A']
    eff       = d['EFF']
    chi2      = d['CHI2']
    z_thick   = d['Z_THICK']
    z_thin    = d['Z_THIN']
    r_thick   = d['R_THICK']
    r_thin    = d['R_THIN']
    chi2_test = d['CHI2_TEST']

loop = np.arange(len(a))

plt.figure(1)
plt.subplot(211)
plt.xlabel('Loop Number')
plt.ylabel(r'$\ R_{0, thick}$ (kpc)')
plt.scatter(loop, r_k, s=1)

plt.subplot(212)
plt.xlabel('Loop Number')
plt.ylabel(r'$\ R_{0, thin}$ (kpc)')
plt.scatter(loop, r_n, s=1)

plt.figure(2)
plt.subplot(211)
plt.xlabel('Loop Number')
plt.ylabel(r'$\ Z_{0, thick}$ (kpc)')
plt.scatter(loop, z_k, s=1)

plt.subplot(212)
plt.xlabel('Loop Number')
plt.ylabel(r'$\ Z_{0, thin}$ (kpc)')
plt.scatter(loop, z_n, s=1)

plt.figure(3)
plt.xlabel('Loop Number')
plt.ylabel('a')
plt.scatter(loop, a, s=1)