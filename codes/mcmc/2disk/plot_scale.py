import numpy as np
from config import *
import matplotlib.pyplot as plt
import matplotlib

'''
Read files of correlation data and plot them, including errors in mean
'''

z_n = np.genfromtxt('Z_THIN1.dat')
z_k = np.genfromtxt('Z_THICK1.dat')
r_n = np.genfromtxt('R_THIN1.dat')
r_k = np.genfromtxt('R_THICK1.dat')
a = np.genfromtxt('A1.dat')

index = np.arange(0, len(a))

plt.figure(1)
#plt.plot(index, z_n, 'ko', index, z_k, 'bo', index, r_n, 'ro', index, r_k, 'go')
#plt.show()
plt.subplot(211)
plt.xlabel(r'$\ R_{0, thin}$ (kpc)')
plt.ylabel(r'$\ R_{0, thick}$ (kpc)')
plt.plot(r_n, r_k, 'ko')

plt.subplot(212)
plt.xlabel(r'$\ Z_{0, thin}$ (kpc)')
plt.ylabel(r'$\ Z_{0, thick}$ (kpc)')
plt.plot(z_n, z_k, 'ko')

plt.show()
#plt.savefig('5sig.png')
