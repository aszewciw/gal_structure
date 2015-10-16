import numpy as np
from config import *
import matplotlib.pyplot as plt
import matplotlib

'''
Read files of correlation data and plot them, including errors in mean
'''

z_n = np.genfromtxt('Z_THN.dat')
z_k = np.genfromtxt('Z_THC.dat')
r_n = np.genfromtxt('R_THN.dat')
r_k = np.genfromtxt('R_THC.dat')
a = np.genfromtxt('A.dat')

print(a)

plt.figure(1)
plt.subplot(211)
plt.xlabel(r'$\ R_{0, thin}$ (kpc)')
plt.ylabel(r'$\ R_{0, thick}$ (kpc)')
plt.plot(r_n, r_k, 'ko')

plt.subplot(212)
plt.xlabel(r'$\ Z_{0, thin}$ (kpc)')
plt.ylabel(r'$\ Z_{0, thick}$ (kpc)')
plt.plot(z_n, z_k, 'ko')
plt.show()
