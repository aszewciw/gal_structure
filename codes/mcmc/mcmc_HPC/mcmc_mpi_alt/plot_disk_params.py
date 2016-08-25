import numpy as np
import matplotlib.pyplot as plt

# # def main():

filename = './data/mcmc_result.dat'
loop, chi2, chi2_r, thin_r0, thin_z0, thick_r0, thick_z0, a = np.genfromtxt(filename, unpack=True)

# Delete first N elements of numpy array
frac_deleted = 0.05
num_deleted  = frac_deleted * len(a)
index_delete = np.arange(num_deleted)
loop         = np.delete(loop, index_delete)
chi2         = np.delete(chi2, index_delete)
chi2_r       = np.delete(chi2_r, index_delete)
thin_r0      = np.delete(thin_r0, index_delete)
thin_z0      = np.delete(thin_z0, index_delete)
thick_r0     = np.delete(thick_r0, index_delete)
thick_z0     = np.delete(thick_z0, index_delete)
a            = np.delete(a, index_delete)

plt.clf()

fig = plt.figure(1)

plt.subplot(211)
plt.xlabel("Thin Disk Scale Height (kpc)")
plt.ylabel("Thick Disk Scale Height (kpc)")
plt.scatter(thin_z0, thick_z0, c=chi2, s=3)
plt.colorbar()

plt.subplot(212)
plt.xlabel("Thin Disk Scale Length (kpc)")
plt.ylabel("Thick Disk Scale Length (kpc)")
plt.scatter(thin_r0, thick_r0, c=chi2, s=3)
plt.colorbar()



plt.figure(2)
plt.subplot(321)
# plt.xlabel("Loop Number")
# plt.xticks(x)
plt.ylabel("Thin Sc Height (kpc)")
plt.scatter(loop, thin_z0, c=chi2, s=2)
# plt.axis([0, len(loop), min(thin_z0), max(thin_z0)])

plt.subplot(322)
# plt.xlabel("Loop Number")
# plt.xticks(x)
plt.ylabel("Thick Sc Height (kpc)")
plt.scatter(loop, thick_z0, c=chi2, s=2)
# plt.axis([0, len(loop), min(thick_z0), max(thick_z0)])

plt.subplot(323)
# plt.xlabel("Loop Number")
# plt.xticks(x)
plt.ylabel("Thin Sc Length (kpc)")
plt.scatter(loop, thin_r0, c=chi2, s=2)
# plt.axis([0, len(loop), min(thin_r0), max(thin_r0)])

plt.subplot(324)
plt.xlabel("Loop Number")
# plt.xticks(x)
plt.ylabel("Thick Sc Length (kpc)")
plt.scatter(loop, thick_r0, c=chi2, s=2)
# plt.axis([0, len(loop), min(thick_r0), max(thick_r0)])

plt.subplot(325)
plt.xlabel("Loop Number")
# plt.xticks(x)
plt.ylabel("Thick:thin ratio")
plt.scatter(loop, a, c=chi2, s=2)
# plt.axis([0, len(loop), min(a), max(a)])
plt.colorbar()

plt.show()
plt.clf()
