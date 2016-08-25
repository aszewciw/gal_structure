import numpy as np
from config import *
import matplotlib.pyplot as plt

# # def main():

filename = out_dir + 'mcmc_result.dat'

loop, r_thin, z_thin, r_thick, z_thick, a, chi2, dof, chi_dof = np.genfromtxt(
    filename, unpack=True)

length = 50000

# Delete first N elements of numpy array
frac_deleted = 0.05
num_deleted  = frac_deleted * length
index_delete = np.arange(num_deleted)
chi2         = chi2[num_deleted:49999]
z_thick      = z_thick[num_deleted:49999]
z_thin       = z_thin[num_deleted:49999]
a            = a[num_deleted:49999]
r_thin       = r_thin[num_deleted:49999]
r_thick      = r_thick[num_deleted:49999]
loop         = loop[num_deleted:49999]
# chi2         = np.delete(chi2, index_delete)
# z_thick      = np.delete(z_thick, index_delete)
# z_thin       = np.delete(z_thin, index_delete)
# r_thick      = np.delete(r_thick, index_delete)
# r_thin       = np.delete(r_thin, index_delete)
# a            = np.delete(a, index_delete)
# loop         = np.delete(loop, index_delete)

plt.clf()


plt.figure(1)
plt.subplot(211)
plt.xlabel("Thin Disk Scale Height (kpc)")
plt.ylabel("Thick Disk Scale Height (kpc)")
plt.scatter(z_thin, z_thick, c=chi2, s=3)
plt.colorbar()

plt.subplot(212)
plt.xlabel("Thin Disk Scale Length (kpc)")
plt.ylabel("Thick Disk Scale Length (kpc)")
plt.scatter(r_thin, r_thick, c=chi2, s=3)
plt.colorbar()
plt.savefig('Scales_qiqi_50K.png')


x = [0, 25000, 50000]

plt.figure(2)
plt.subplot(321)
# plt.xlabel("Loop Number")
plt.xticks(x)
plt.ylabel("Thin Sc Height (kpc)")
plt.scatter(loop, z_thin, c=chi2, s=2)
# plt.axis([0, len(loop), min(z_thin), max(z_thin)])

plt.subplot(322)
# plt.xlabel("Loop Number")
plt.xticks(x)
plt.ylabel("Thick Sc Height (kpc)")
plt.scatter(loop, z_thick, c=chi2, s=2)
# plt.axis([0, len(loop), min(z_thick), max(z_thick)])

plt.subplot(323)
# plt.xlabel("Loop Number")
plt.xticks(x)
plt.ylabel("Thin Sc Length (kpc)")
plt.scatter(loop, r_thin, c=chi2, s=2)
# plt.axis([0, len(loop), min(r_thin), max(r_thin)])

plt.subplot(324)
plt.xlabel("Loop Number")
plt.xticks(x)
plt.ylabel("Thick Sc Length (kpc)")
plt.scatter(loop, r_thick, c=chi2, s=2)
# plt.axis([0, len(loop), min(r_thick), max(r_thick)])

plt.subplot(325)
plt.xlabel("Loop Number")
plt.xticks(x)
plt.ylabel("Thick:thin ratio")
plt.scatter(loop, a, c=chi2, s=2)
# plt.axis([0, len(loop), min(a), max(a)])
plt.colorbar()
plt.savefig("loops_chi2_qiqi_50K.png")

plt.show()
plt.clf()
