import numpy as np
from config import *
import matplotlib.pyplot as plt

filename = str(input('Enter filename with .npz extension: '))

filename = mcmcdata_dir + filename

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
plt.scatter(loop, r_thick, s=1)

plt.subplot(212)
plt.xlabel('Loop Number')
plt.ylabel(r'$\ R_{0, thin}$ (kpc)')
plt.scatter(loop, r_thin, s=1)
plt.savefig('mock_rk_rn.png')

plt.figure(2)
plt.subplot(211)
plt.xlabel('Loop Number')
plt.ylabel(r'$\ Z_{0, thick}$ (kpc)')
plt.scatter(loop, z_thick, s=1)

plt.subplot(212)
plt.xlabel('Loop Number')
plt.ylabel(r'$\ Z_{0, thin}$ (kpc)')
plt.scatter(loop, z_thin, s=1)
plt.savefig('mock_zk_zn.png')

plt.figure(3)
plt.xlabel('Loop Number')
plt.ylabel('a')
plt.scatter(loop, a, s=1)
plt.savefig('mock_a.png')

plt.figure(4)
plt.xlabel('Loop Number')
plt.ylabel('chi2 (red) and possible chi2')
plt.scatter(loop, chi2, color='r', s=1)
plt.scatter(loop, chi2_test, color='b', s=1)
plt.savefig('mock_chi2.png')


plt.figure(5)
plt.xlabel('Loop Number')
plt.ylabel('Efficiency')
plt.scatter(loop, eff, s=1)
plt.savefig('mock_eff.png')