import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


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


# xmin = thin_z0.min()
# xmax = thin_z0.max()
# ymin = thick_z0.min()
# ymax = thick_z0.max()

# X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
# positions = np.vstack([X.ravel(), Y.ravel()])
# values = np.vstack([thin_z0, thick_z0])
# kernel = stats.gaussian_kde(values)
# Z = np.reshape(kernel(positions).T, X.shape)


# plt.clf()
# fig, ax = plt.subplots()
# ax.imshow(np.rot90(Z), cmap=plt.cm.gist_earth_r,
#     extent=[xmin, xmax, ymin, ymax])
# ax.plot(thin_z0, thick_z0, 'k.', markersize=2)
# ax.set_xlim([xmin, xmax])
# ax.set_ylim([ymin, ymax])
# plt.savefig('bleh.png')




# '''below is old code'''

index_min = np.argmin(chi2)
z0_thin_true  = 0.233
r0_thin_true  = 2.34
z0_thick_true = 0.674
r0_thick_true = 2.51
ratio_true    = 0.1


# print(thin_z0[index_min])
# print(thin_r0[index_min])
# print(thick_z0[index_min])
# print(thick_r0[index_min])
# print(a[index_min])

plt.clf()


plt.figure(1)
plt.xlabel("Thin Disk Scale Height (kpc)")
plt.ylabel("Thick Disk Scale Height (kpc)")
plt.scatter(thin_z0, thick_z0, c=chi2, s=3)
plt.colorbar()
# plt.scatter(thin_z0[index_min], thick_z0[index_min], c='m', marker='*', s=1000)
plt.scatter(z0_thin_true, z0_thick_true, c='m', marker='*', s=1000)
plt.axes().set_aspect('equal', 'datalim')
plt.axis([min(thin_z0), max(thin_z0), min(thick_z0), max(thick_z0)])
plt.savefig('density_heights.png')

plt.figure(2)
plt.xlabel("Thin Disk Scale Length (kpc)")
plt.ylabel("Thick Disk Scale Length (kpc)")
plt.scatter(thin_r0, thick_r0, c=chi2, s=3)
plt.colorbar()
# plt.scatter(thin_r0[index_min], thick_r0[index_min], c='m', marker='*', s=1000)
plt.scatter(r0_thin_true, r0_thick_true, c='m', marker='*', s=1000)
plt.axes().set_aspect('equal', 'datalim')
plt.axis([min(thin_r0), max(thin_r0), min(thick_r0), max(thick_r0)])
plt.savefig('density_lengths.png')


x = np.array([0, 100000, 200000, 300000])

plt.figure(3)

plt.subplot(321)
plt.ylabel("Thin Sc Height (kpc)")
plt.scatter(loop, thin_z0, c=chi2, s=2)
plt.axis([loop_start, loop_end, min(thin_z0), max(thin_z0)])
plt.xticks(x)

plt.subplot(322)
plt.ylabel("Thick Sc Height (kpc)")
plt.scatter(loop, thick_z0, c=chi2, s=2)
plt.axis([loop_start, loop_end, min(thick_z0), max(thick_z0)])
plt.xticks(x)

plt.subplot(323)
plt.ylabel("Thin Sc Length (kpc)")
plt.scatter(loop, thin_r0, c=chi2, s=2)
plt.axis([loop_start, loop_end, min(thin_r0), max(thin_r0)])
plt.xticks(x)

plt.subplot(324)
plt.xlabel("Loop Number")
plt.ylabel("Thick Sc Length (kpc)")
plt.scatter(loop, thick_r0, c=chi2, s=2)
plt.axis([loop_start, loop_end, min(thick_r0), max(thick_r0)])
plt.xticks(x)

plt.subplot(325)
plt.xlabel("Loop Number")
plt.ylabel("Thick:thin ratio")
plt.scatter(loop, a, c=chi2, s=2)
plt.axis([loop_start, loop_end, min(a), max(a)])
plt.xticks(x)
plt.colorbar()

plt.savefig('density_steps.png')

# plt.show()
plt.clf()
