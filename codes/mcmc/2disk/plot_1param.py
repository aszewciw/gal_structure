import numpy as np
from config import *
import matplotlib.pyplot as plt

# def main():

filename = str(input('Enter filename with .npz extension: '))
filename = mcmcdata_dir + filename
param = str(input('Which parameter? '))

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

if param == 'a':
    pltparam = a
elif param == 'z_thick':
    pltparam = z_thick
elif param == 'z_thin':
    pltparam = z_thin
elif param == 'r_thin':
    pltparam = r_thin
elif param == 'r_thick':
    pltparam = r_thick
else:
    print('Incorrect parameter input')


plt.figure(1)
plt.xlabel(param)
plt.ylabel('chi^2')
# plt.yscale('log')
plt.scatter(pltparam, chi2, s=1)
# plt.axis([0, len(loop), 0, 1000])
# # plt.savefig('mock_chi2.png')



plt.show()

