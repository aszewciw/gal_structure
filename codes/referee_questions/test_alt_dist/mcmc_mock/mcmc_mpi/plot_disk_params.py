import numpy as np
import matplotlib.pyplot as plt

# # def main():

filename = '../data/mcmc_output/mcmc_result.dat'

loop, chi2, chi2_r, thin_r0, thin_z0, thick_r0, thick_z0, a = np.genfromtxt(filename, unpack=True)

loop_start = min(loop)
loop_end = max(loop)

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

index_min = np.argmin(chi2)

z0_thin_true  = 0.2
r0_thin_true  = 1.0
z0_thick_true = 0.3
r0_thick_true = 2.0
ratio_true    = 0.2
plt.clf()


# plt.subplot(211)
plt.figure(1)
plt.title('MCMC results on meaningless density profile')
plt.xlabel("Pop. 1 Z1 (kpc)")
plt.ylabel("Pop. 2 Z2 (kpc)")
plt.scatter(thin_z0, thick_z0, c=chi2, s=3)
plt.colorbar()
plt.scatter(thin_z0[index_min], thick_z0[index_min], c='m', marker='*', s=1000)
plt.scatter(z0_thin_true, z0_thick_true, c='m', marker='x', s=1000)
plt.axes().set_aspect('equal', 'datalim')
plt.axis([min(thin_z0), max(thin_z0), min(thick_z0), max(thick_z0)])
plt.savefig('fake_pop_heights.png')


plt.figure(2)
plt.title('MCMC results on meaningless density profile')
plt.xlabel("Pop. 1 R1 (kpc)")
plt.ylabel("Pop. 2 R2 (kpc)")
plt.scatter(thin_r0, thick_r0, c=chi2, s=3)
plt.colorbar()
plt.scatter(thin_r0[index_min], thick_r0[index_min], c='m', marker='*', s=1000)
plt.scatter(r0_thin_true, r0_thick_true, c='m', marker='x', s=1000)
plt.axes().set_aspect('equal', 'datalim')
plt.axis([min(thin_r0), max(thin_r0), min(thick_r0), max(thick_r0)])
plt.savefig('fake_pop_lengths.png')


x = np.array([0, 100000, 200000, 300000, 400000])

plt.figure(3)
plt.subplot(321)
plt.ylabel("Z1 (kpc)")
plt.scatter(loop, thin_z0, c=chi2, s=2)
plt.axis([loop_start, loop_end, min(thin_z0), max(thin_z0)])
plt.xticks(x)

plt.subplot(322)
plt.ylabel("Z2 (kpc)")
plt.scatter(loop, thick_z0, c=chi2, s=2)
plt.axis([loop_start, loop_end, min(thick_z0), max(thick_z0)])
plt.xticks(x)

plt.subplot(323)
plt.ylabel("R1 (kpc)")
plt.scatter(loop, thin_r0, c=chi2, s=2)
plt.axis([loop_start, loop_end, min(thin_r0), max(thin_r0)])
plt.xticks(x)

plt.subplot(324)
plt.xlabel("Loop Number")
plt.ylabel("R2 (kpc)")
plt.scatter(loop, thick_r0, c=chi2, s=2)
plt.axis([loop_start, loop_end, min(thick_r0), max(thick_r0)])
plt.xticks(x)

plt.subplot(325)
plt.xlabel("Loop Number")
plt.ylabel("Pop2:Pop1 ratio")
plt.scatter(loop, a, c=chi2, s=2)
plt.axis([loop_start, loop_end, min(a), max(a)])
plt.xticks(x)
plt.colorbar()

plt.savefig('fake_pop_steps.png')

plt.show()
plt.clf()
