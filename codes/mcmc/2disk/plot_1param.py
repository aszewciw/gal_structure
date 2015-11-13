import numpy as np
from config import *
import matplotlib.pyplot as plt

# def main():

filename = str(input('Enter filename with .npz extension: '))
filename = mcmcdata_dir + filename
param = str(input('Which parameter? '))

with np.load(filename) as d:
    chi2      = d['CHI2']

    if param == 'a':
        pltparam = d['A']
    elif param == 'z_thick':
        pltparam = d['Z_THICK']
    elif param == 'z_thin':
        pltparam = d['Z_THIN']
    elif param == 'r_thin':
        pltparam = d['R_THIN']
    elif param == 'r_thick':
        pltparam = d['R_THICK']
    else:
        print('Incorrect parameter input')

loop = np.arange(len(pltparam))

plt.figure(1)
plt.xlabel(param)
plt.ylabel('chi^2')
# plt.yscale('log')
plt.scatter(pltparam, chi2, s=1)
# plt.axis([0, len(loop), 0, 1000])
# # plt.savefig('mock_chi2.png')



plt.show()

