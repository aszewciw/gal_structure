import numpy as np
from config import *
import matplotlib.pyplot as plt

# def main():

# filename = str(input('Enter filename with .npz extension: '))
filename = 'victor_test.npz'
# filename = mcmcdata_dir + filename

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

diff = chi2_test - chi2

# count = 0
# for i in loop:
#     if diff[i] == 0:
#         print(i, diff[i])
#         count +=1
plt.figure(1)
plt.subplot(211)
plt.xlabel('Loop Number')
plt.ylabel(r'$\ R_{0, thick}$ (kpc)')
plt.scatter(loop, r_thick, s=1)

plt.subplot(212)
plt.xlabel('Loop Number')
plt.ylabel(r'$\ R_{0, thin}$ (kpc)')
plt.scatter(loop, r_thin, s=1)
# plt.savefig('mock_rk_rn.png')

plt.figure(2)
plt.subplot(211)
plt.xlabel('Loop Number')
plt.ylabel(r'$\ Z_{0, thick}$ (kpc)')
plt.scatter(loop, z_thick, s=1)

plt.subplot(212)
plt.xlabel('Loop Number')
plt.ylabel(r'$\ Z_{0, thin}$ (kpc)')
plt.scatter(loop, z_thin, s=1)
# plt.savefig('mock_zk_zn.png')

plt.figure(3)
plt.xlabel('Loop Number')
plt.ylabel('a')
plt.scatter(loop, a, s=1)
# plt.savefig('mock_a.png')

# plt.figure(1)
# plt.xlabel('Loop Number')
# plt.ylabel('chi2 proposed - chi2 accepted')
# # plt.yscale('log')
# plt.scatter(loop, chi2, s=1)
# plt.axis([0, len(loop), 0, 1000])
# # plt.savefig('mock_chi2.png')

# plt.figure(4)
# plt.xlabel('Loop')
# plt.ylabel('chi2')
# plt.scatter(loop, chi2, s=1)

# plt.figure(5)
# plt.xlabel('Loop Number')
# plt.ylabel('Efficiency')
# plt.scatter(loop, eff, s=1)
# plt.savefig('mock_eff.png')

plt.show()

# print(chi2, chi2_test)

# if __name__ == '__main__':
#     main()

