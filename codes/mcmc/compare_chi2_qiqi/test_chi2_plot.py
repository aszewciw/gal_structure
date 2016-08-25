import numpy as np
from config import *
import matplotlib.pyplot as plt

# def main():

# filename = str(input('Enter filename with .npz extension: '))
filename = out_dir + 'chi2_test.npz'
# filename = mcmcdata_dir + filename

with np.load(filename) as d:

    chi2       = d['CHI2_LOS_BIN']
    mm         = d['MM']
    dd         = d['DD']
    los        = d['LOS_NUM']
    bin_num    = d['BIN_NUM']
    uni_jk_err = d['UNI_JK_ERR']
    dat_jk_err = d['DAT_JK_ERR']


total_bins    = len(chi2)
index         = np.arange(total_bins)

count_chi2_0  = 0
count_DD_0    = 0
count_DDerr_0 = 0
count_both    = 0


for i in range(total_bins):

    if chi2[i] == 0.0:

        count_chi2_0 += 1

        if dd[i] == 0.0:

            count_DD_0 += 1

            if dat_jk_err[i] == 0.0:

                count_both += 1

        if dat_jk_err[i] == 0.0:

            count_DDerr_0 += 1


print('Total Number of bins is ', total_bins)
print('Number of times chi2=0 is ', count_chi2_0)
print('Number of times DD=0 is ', count_DD_0)
print('Number of times err=0 is ', count_DDerr_0)
print('Number of times both are 0 is ', count_both)

        # print('Line of sight ', los[i])
        # print('Bin number ', bin_num[i])
        # print('MM is ', mm[i])
        # print('DD is ', dd[i])
        # print('Uniform error is ', uni_jk_err[i])
        # print('Data error is ', dat_jk_err[i])

