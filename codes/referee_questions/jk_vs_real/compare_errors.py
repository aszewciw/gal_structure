import numpy as np
import os, sys, math
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------#
'''
Compare the actual errors of normalized pair counts for SEGUE mocks.

The jackknife error files are ascii files with column index 7 containing the
fractional error.
This must be multiplied by the normalized pair count of the mock.

The real error files contain the normalized standard deviation as the index 2
column.
'''

#------------------------------------------------------------------------------#

# Directories
raw_dir   = '../data/'
stats_dir = '../1000_mocks_cut/errors_pairs/data/mean_var_std/'
mcmc_dir  = '../mcmc_mock/data/'
jk_dir    = mcmc_dir + 'jackknife/'
dd_dir    = mcmc_dir + 'mock_dd/'
bins_dir  = mcmc_dir + 'rbins/'

#------------------------------------------------------------------------------#

def main():

    # Load pointing list
    todo_file = raw_dir + 'todo_list.ascii.dat'
    ID_list   = np.genfromtxt(todo_file, dtype=int, usecols=[0], unpack=True,
                skip_header=1)
    N_los = len(ID_list)

    # Load lower, upper, and middle of bins for plotting
    bins_file = bins_dir + 'rbins.ascii.dat'
    bins_l, bins_u, bins_c = np.genfromtxt(bins_file, skip_header=1, unpack=True,
                                usecols=[0,1,2])
    Nbins = len(bins_c)

    # Store all values in an array
    ratio_list = np.zeros((N_los, Nbins))

    # Initialize plot
    plt.clf()
    plt.figure(1)

    # Loop over pointings
    for j in range(N_los):

        ID = str(ID_list[j])

        # load real standard deviation
        real_file = stats_dir + 'stats_' + ID + '.dat'
        std_real  = np.genfromtxt(real_file, unpack=True, usecols=[2])

        # load fractional jackknife errors
        jk_file     = jk_dir + 'mock_' + ID + '_jk_error.dat'
        frac_err_jk = np.genfromtxt(jk_file, unpack=True, usecols=[7])

        # load mock dd counts to calculate jk standard deviation
        dd_file = dd_dir + 'dd_' + ID + '.dat'
        dd      = np.genfromtxt(dd_file)

        # Calculate jk standard dev
        std_jk = dd * frac_err_jk

        # Initialize array of ratios
        error_ratio = np.zeros(Nbins)

        # Calculate ratio of fractional errors
        for i in range(Nbins):
            # Avoid division by zero
            if std_real[i]==0:
                continue
            error_ratio[i] = std_jk[i] / std_real[i]

        ratio_list[j,:] = error_ratio

        plt.semilogx(bins_c, error_ratio, '0.75', zorder=-40)

    frac_median = np.median(ratio_list, axis=0)
    lower_16    = np.percentile(ratio_list, 16, axis=0)
    lower_84    = np.percentile(ratio_list, 84, axis=0)
    upper_error = lower_84 - frac_median
    lower_error = frac_median - lower_16
    errorbars   = [lower_error, upper_error]
    plt.errorbar(bins_c, frac_median, yerr=errorbars, fmt='ro', ecolor = 'r',
        elinewidth = 1.5, capthick = 1.5, capsize = 7)
    # plt.plot(bins, frac_median, 'ro')
    # plt.plot(bins, lower_16, 'ro')
    # plt.plot(bins, lower_84, 'ro')
    # frac_mean = np.median(ratio_list, axis=0)
    # frac_std  = np.std(ratio_list, axis=0)
    # errorbars2 = frac_std / math.sqrt(N_los)
    # plt.errorbar(bins_c, frac_median, yerr=errorbars2, fmt='bo', ecolor = 'b',
    #     elinewidth = 1.5, capthick = 1.5, capsize = 7)

    plt.axis([bins_l[0], bins_u[-1], 0, 2])
    plt.xlabel('Radial bin center (kpc)')
    plt.ylabel(r'$\displaystyle\frac{\sigma_{jk}}{\sigma_{real}}$')
    plt.title('Ratio of standard deviations across 152 l.o.s.')

    fig_name = 'real_ratios.png'
    plt.savefig(fig_name)
    plt.show()
    plt.clf()

if __name__ == '__main__':
    main()

