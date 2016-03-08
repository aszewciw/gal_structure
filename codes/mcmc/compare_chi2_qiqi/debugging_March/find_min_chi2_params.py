import matplotlib.pyplot as plt
import numpy as np
from config import *

#find parameters for Qingqing's minimum chi2 value

qiqi_file = out_dir + 'mcmc_result.dat'
my_file   = out_dir + 'test.dat'

rthin, zthin, rthick, zthick, a, chi2 = np.genfromtxt(qiqi_file, unpack=True, usecols=[1, 2, 3, 4, 5, 6])

min_index = np.argmin(chi2)

print('Best chi2 is:   ', chi2[min_index])
print('Best rthin is:  ', rthin[min_index])
print('Best zthin is:  ', zthin[min_index])
print('Best rthick is: ', rthick[min_index])
print('Best zthick is: ', zthick[min_index])
print('Best a is:      ', a[min_index])