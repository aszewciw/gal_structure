import numpy as np
# import matplotlib.pyplot as plt
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

std_thin_r0 = np.std(thin_r0)
std_thin_z0 = np.std(thin_z0)
std_thick_r0 = np.std(thick_r0)
std_thick_z0 = np.std(thick_z0)
std_ratio = np.std(a)

print(std_thin_z0)
print(std_thin_r0)
print(std_thick_z0)
print(std_thick_r0)
print(std_ratio)