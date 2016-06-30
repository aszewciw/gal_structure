# import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
sns.set(style="white")

# Generate a random correlated bivariate dataset
# rs = np.random.RandomState(5)
# mean = [0, 0]
# cov = [(1, .5), (.5, 1)]
# x1, x2 = rs.multivariate_normal(mean, cov, 500).T
# x1 = pd.Series(x1, name="$X_1$")
# x2 = pd.Series(x2, name="$X_2$")

# Show the joint distribution using kernel density estimation
# g = sns.jointplot(x1, x2, kind="kde", size=7, space=0)

# plt.show()
# # # def main():

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

# std_thin_r0 = np.std(thin_r0)
# std_thin_z0 = np.std(thin_z0)
# std_thick_r0 = np.std(thick_r0)
# std_thick_z0 = np.std(thick_z0)
# std_ratio = np.std(a)

# g = sns.jointplot(thin_z0, thick_z0, kind="kde", size=7, space=0)
# plt.show()

# x,y=np.random.randn(2,10000)
# x = thin_z0
# y = thick_z0
x = thin_r0
y = thick_r0

fig,ax=plt.subplots()
plt.scatter(x,y,s=2,color='cyan')
sns.kdeplot(x,y, shade=False,shade_lowest=False, ax=ax,n_levels=3,cmap="Purples_d")
# sns.kdeplot(x,y, shade=False,shade_lowest=False, ax=ax,cmap="Purples_d")
plt.axis([min(x),max(x),min(y),max(y)])
# plt.title('Scale Lengths')
# plt.xlabel('r0_thin (kpc)')
# plt.ylabel('r0_thick (kpc)')
plt.savefig('countour_lengths.png')
# plt.show()
plt.clf()