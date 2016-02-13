import numpy as np
from config import *
import matplotlib.pyplot as plt
import matplotlib

'''
Read files of correlation data and plot them, including errors in mean
'''
choice = 1

<<<<<<< HEAD
if choice == 0:
    z_n = np.genfromtxt('Z_THIN.dat')
    z_k = np.genfromtxt('Z_THICK.dat')
    r_n = np.genfromtxt('R_THIN.dat')
    r_k = np.genfromtxt('R_THICK.dat')
    a = np.genfromtxt('A.dat')
    loop = np.arange(len(a))
elif choice == 1:
    z_n = np.genfromtxt('z_thin2.dat')
    z_k = np.genfromtxt('z_thick2.dat')
    r_n = np.genfromtxt('r_thin2.dat')
    r_k = np.genfromtxt('r_thick2.dat')
    a = np.genfromtxt('a2.dat')
    loop = np.arange(len(a))
else:
    z_n = np.genfromtxt('Z_THIN1.dat')
    z_k = np.genfromtxt('Z_THICK1.dat')
    r_n = np.genfromtxt('R_THIN1.dat')
    r_k = np.genfromtxt('R_THICK1.dat')
    a = np.genfromtxt('A1.dat')
    loop = np.arange(len(a))

# N = len(a)
# acc = 0
# k = 1
# while k < N:
#     if a[k] != a[k-1]:
#         plt.scatter(k, a[k], s=3)
#         acc += 1

#     k += 1

# plt.show()
# print(acc / N)

# plt.figure(1)
# plt.subplot(211)
# plt.xlabel(r'$\ R_{0, thin}$ (kpc)')
# plt.ylabel(r'$\ R_{0, thick}$ (kpc)')
# plt.scatter(r_n, r_k, s=1)

# plt.subplot(212)
# plt.xlabel(r'$\ Z_{0, thin}$ (kpc)')
# plt.ylabel(r'$\ Z_{0, thick}$ (kpc)')
# plt.scatter(z_n, z_k, s=1)
# plt.show()
=======
z_n = np.genfromtxt('Z_THIN1.dat')
z_k = np.genfromtxt('Z_THICK1.dat')
r_n = np.genfromtxt('R_THIN1.dat')
r_k = np.genfromtxt('R_THICK1.dat')
a = np.genfromtxt('A1.dat')

index = np.arange(0, len(a))
>>>>>>> f4ac217758498bce748b8ca9fdb79479b7c92dda

plt.figure(1)
#plt.plot(index, z_n, 'ko', index, z_k, 'bo', index, r_n, 'ro', index, r_k, 'go')
#plt.show()
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
<<<<<<< HEAD
plt.scatter(loop, z_k, s=1)

plt.subplot(212)
plt.xlabel('Loop Number')
plt.ylabel(r'$\ Z_{0, thin}$ (kpc)')
plt.scatter(loop, z_n, s=1)

plt.figure(3)
plt.xlabel('Loop Number')
plt.ylabel('a')
plt.scatter(loop, a, s=1)

# # plt.figure(2)
# # # plt.subplot(212)
# # plt.xlabel(r'$\ Z_{0, thin}$ (kpc)')
# # plt.ylabel(r'$\ Z_{0, thick}$ (kpc)')
# # plt.scatter(z_n, z_k, s=1)

=======
plt.plot(z_n, z_k, 'ko')
>>>>>>> f4ac217758498bce748b8ca9fdb79479b7c92dda

plt.show()
#plt.savefig('5sig.png')
