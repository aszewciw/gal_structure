import numpy as np
import matplotlib.pyplot as plt

# # def main():

filename = './data/mcmc_result.dat'
step, chi2, chi2_r, thin_r0, thin_z0, thick_r0, thick_z0, a = np.genfromtxt(filename, unpack=True)

# Delete first N elements of numpy array
frac_deleted = 0.05
num_deleted  = frac_deleted * len(a)
index_delete = np.arange(num_deleted)
step         = np.delete(step, index_delete)
chi2         = np.delete(chi2, index_delete)
chi2_r       = np.delete(chi2_r, index_delete)
thin_r0      = np.delete(thin_r0, index_delete)
thin_z0      = np.delete(thin_z0, index_delete)
thick_r0     = np.delete(thick_r0, index_delete)
thick_z0     = np.delete(thick_z0, index_delete)
a            = np.delete(a, index_delete)

plt.clf()

fig = plt.figure()
ax1 = fig.add_subplot(211, aspect='equal')

# plt.subplot(211, aspect='equal')
plt.xlabel("Thin Disk Scale Height (kpc)")
plt.ylabel("Thick Disk Scale Height (kpc)")
plt.scatter(thin_z0, thick_z0, c=chi2, s=3)
plt.colorbar()

ax2 = fig.add_subplot(212, aspect='equal')
# plt.subplot(212, aspect='equal')
plt.xlabel("Thin Disk Scale Length (kpc)")
plt.ylabel("Thick Disk Scale Length (kpc)")
plt.scatter(thin_r0, thick_r0, c=chi2, s=3)
plt.colorbar()



# plt.figure(2)
# plt.subplot(321)
# # plt.xlabel("Loop Number")
# plt.xticks(x)
# plt.ylabel("Thin Sc Height (kpc)")
# plt.scatter(loop, z_thin, c=chi2, s=2)
# # plt.axis([0, len(loop), min(z_thin), max(z_thin)])

# plt.subplot(322)
# # plt.xlabel("Loop Number")
# plt.xticks(x)
# plt.ylabel("Thick Sc Height (kpc)")
# plt.scatter(loop, z_thick, c=chi2, s=2)
# # plt.axis([0, len(loop), min(z_thick), max(z_thick)])

# plt.subplot(323)
# # plt.xlabel("Loop Number")
# plt.xticks(x)
# plt.ylabel("Thin Sc Length (kpc)")
# plt.scatter(loop, r_thin, c=chi2, s=2)
# # plt.axis([0, len(loop), min(r_thin), max(r_thin)])

# plt.subplot(324)
# plt.xlabel("Loop Number")
# plt.xticks(x)
# plt.ylabel("Thick Sc Length (kpc)")
# plt.scatter(loop, r_thick, c=chi2, s=2)
# # plt.axis([0, len(loop), min(r_thick), max(r_thick)])

# plt.subplot(325)
# plt.xlabel("Loop Number")
# plt.xticks(x)
# plt.ylabel("Thick:thin ratio")
# plt.scatter(loop, a, c=chi2, s=2)
# # plt.axis([0, len(loop), min(a), max(a)])
# plt.colorbar()

plt.show()
plt.clf()
