import numpy as np
import sys
import matplotlib.pyplot as plt

data_dir = '../data/mcmc_output/'
raw_dir = '../../data/'

'''
Load stat data for true parameters.
'''

# File of chi2 values for true parameters
truth_file = data_dir + 'chi2_truth.dat'
los_t, bin_t, corr_t, sigma2_t, chi2_t = np.loadtxt(truth_file, unpack=True,
                                            delimiter='\t', dtype=None)
# Recast beacause fuck numpy
los_t = los_t.astype(int)
bin_t = bin_t.astype(int)

'''
Load stat data for best-fit parameters.
'''

# File of chi2 values for best fit parameters
best_file = data_dir + 'chi2_best.dat'
los_b, bin_b, corr_b, sigma2_b, chi2_b = np.loadtxt(best_file, unpack=True,
                                            delimiter='\t', dtype=None)
# Recast because fuck numpy
los_b = los_b.astype(int)
bin_b = bin_b.astype(int)

'''
Load pointing data
'''
todo_file = raw_dir + 'todo_list.ascii.dat'
ID, ra, dec, Nstars = np.genfromtxt(todo_file, skip_header=1, unpack=True, usecols=[0,1,2,10])

N_los  = len(np.unique(los_b))
N_bins = len(np.unique(bin_b))


'''
Process data for plotting
'''

# Find differences in chi2 (where truth is higher than best)
chi2_diff = chi2_t - chi2_b

# Rank chi2 differences from highest to lowest
chi2_diff_ranks = np.flipud(np.argsort(chi2_diff,axis=0))

# Get total chi2
tot_chi2_t = np.sum(chi2_t)
tot_chi2_b = np.sum(chi2_b)
tot_chi2_d = np.sum(chi2_diff)

# See fractional contributions to whole difference (some will be negative)
chi2_diff_frac = chi2_diff / tot_chi2_d
diff_reshaped  = chi2_diff_frac.reshape(N_los, N_bins)

# Rank chi2 differences from highest to lowest
chi2_diff_ranks = np.flipud(np.argsort(chi2_diff_frac,axis=0))


'''
Figure 1

Colormapping fractional chi2 difference on a plot of bin # vs los #
'''


plt.clf()
plt.figure(1)
plt.scatter(los_b, bin_b, c=chi2_diff_frac, cmap='Blues', s=100)
plt.title('bin vs. los colored by chi2 fractional difference')
plt.xlabel('Line of sight')
plt.ylabel('Bin Number')

plt.colorbar()
plt.savefig('chi2_diff.png')
# plt.show()

plt.clf()

'''
Figure 2

Plot fractional chi2 difference sums for each bin
'''
bin_sums = np.sum(diff_reshaped, axis=0)

# plt.clf()
plt.figure(2)
plt.title('chi2 fractional difference sums for each radial bin ')
plt.xlabel('Bin number')
plt.ylabel('chi2 fractional difference sum')
plt.plot(np.arange(N_bins), bin_sums)
plt.savefig('bin_sums.png')
# plt.show()
plt.clf()

'''
Figure 3

Plot fractional chi2 difference sums for each los
'''

los_sums = np.sum(diff_reshaped, axis=1)

# plt.clf()
plt.figure(3)
plt.title('chi2 fractional difference sums for each l.o.s. ')
plt.xlabel('Pointing ID')
plt.ylabel('chi2 fractional difference sum')
plt.plot(ID, los_sums)
plt.savefig('los_sums.png')
# plt.show()
# plt.clf()

'''
Figure 4

Plot frac difference vs. corr difference
'''

corr_sqdiff = (corr_t-1)**2 - (corr_b-1)**2

# plt.clf()
plt.figure(4)
plt.scatter(corr_sqdiff, chi2_diff_frac, s=3)
plt.title('chi2 fractional difference vs. corr difference')
plt.xlabel(r'$corr_{true} - corr_{best}$')
plt.ylabel('chi2 fractional difference sum')
# plt.axis([-0.5,0.5,-0.02,0.02])
plt.savefig('chi_vs_corr.png')
# plt.show()
# plt.clf()

'''
Figure 5

Plot frac difference vs. sigma^2 difference
'''
sigma2_t_inv = np.zeros(len(sigma2_t))
sigma2_b_inv = np.zeros(len(sigma2_b))

for i in range(len(sigma2_b)):
    if sigma2_t[i] != 0.0:
        sigma2_t_inv[i] = 1/sigma2_t[i]
    if sigma2_b[i] != 0.0:
        sigma2_b_inv[i] = 1/sigma2_b[i]


sigma2_diff = sigma2_t_inv - sigma2_b_inv

plt.figure(5)
plt.scatter(sigma2_diff, chi2_diff_frac, s=3)
plt.title('chi2 fractional difference vs. 1/sigma2 difference')
plt.xlabel(r'$1/sig2_{true} - 1/sig2_{best}$')
plt.ylabel('chi2 fractional difference sum')
# plt.axis([-0.5,0.5,-0.02,0.02])
plt.savefig('chi_vs_sig2.png')
# plt.show()
# plt.clf()


'''
Figure 6

Plot ra-dec color-coded by chi2 difference contribution
'''

plt.figure(6)
plt.title('dec vs ra colored by chi2/los')
plt.xlabel('ra')
plt.ylabel('dec')
plt.scatter(ra, dec, c=los_sums, s=50)
plt.colorbar()
plt.savefig('ra_vs_dec.png')
# plt.show()
plt.clf()


'''
Figure 6

chi2 difference los sum vs Nstars
'''

plt.figure(7)
plt.title('chi2 difference per los vs Nstars')
plt.xlabel('Nstars')
plt.ylabel('fractional chi2')
plt.scatter(Nstars, los_sums, s=3)
plt.savefig('nstars.png')
plt.clf()


plt.figure(8)
plt.subplot(221)
plt.xlabel('Bin number')
plt.ylabel('chi2 fractional difference sum')
plt.plot(np.arange(N_bins), bin_sums)

plt.subplot(222)
plt.xlabel('Pointing ID')
plt.ylabel('chi2 fractional difference sum')
plt.plot(ID, los_sums)

plt.subplot(223)
plt.xlabel('ra')
plt.ylabel('dec')
plt.scatter(ra, dec, c=los_sums, s=50)
plt.colorbar()

plt.subplot(224)
plt.xlabel('Nstars')
plt.ylabel('fractional chi2')
plt.scatter(Nstars, los_sums, s=3)
plt.tight_layout()
plt.savefig('chi2_differences.png')