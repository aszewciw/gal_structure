import matplotlib.pyplot as plt
import numpy as np
from config import *

qiqi_file = out_dir + 'mcmc_result.dat'
my_file   = out_dir + 'chi2_Mar10.dat'

chi2      = np.genfromtxt(qiqi_file, unpack=True, usecols=[6])
chi2_me   = np.genfromtxt(my_file)

chi2_qiqi = []

loops = np.arange(len(chi2))

for i in range(len(chi2_me)):

    chi2_qiqi.append(chi2[i])

chi2_qiqi = np.asarray(chi2_qiqi)
loop      = np.arange(len(chi2_me))
diff      = chi2_me - chi2_qiqi

plt.clf()
plt.figure(1)
plt.plot(loop, diff, 'g')
# plt.plot(loops, chi2)

plt.show()

