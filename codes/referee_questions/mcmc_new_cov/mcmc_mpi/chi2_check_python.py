import pandas as pd
from scipy import linalg
import numpy as np

rawdata_dir  = '../../data/'
data_dir     = '../data/'
mock_dir     = '../../prepare_mock/data/'
uni_dir      = '../../prepare_randoms/data/'
errors_dir   = data_dir + 'errors/'
mcmc_out_dir = data_dir + 'mcmc_output/'
mock_dd_dir  = data_dir + 'mock_dd/'
pairs_dir    = data_dir + 'model_pairs/'
zrw_dir      = data_dir + 'model_positions/'
rbins_dir    = data_dir + 'rbins/'
sigma_dir    = '../../1000_mocks_cut/errors_pairs/data/mean_var_std/'
counts_dir   = '../../1000_mocks_cut/errors_pairs/data/'


def main():

    # Load list of pointing IDs
    todo_file = rawdata_dir + 'todo_list.ascii.dat'
    ID_list   = np.genfromtxt(todo_file, skip_header=1, usecols=[0], unpack=True,
                            dtype=str)
    N_los = len(ID_list)

    # Load bins centers
    bins_file   = rbins_dir + 'rbins.ascii.dat'
    bin_centers = np.genfromtxt(bins_file, skip_header=1, usecols=[2], unpack=True)
    N_bins      = len(bin_centers)

    # Round bin centers to three decimal places
    bin_centers = np.round(bin_centers, 3)

    # Make array of column names for pandas Dataframe
    col_names = []

    for i in range(N_bins):
        name = str(bin_centers[i])
        col_names.append(name)

    # Recast as array
    col_names = np.asarray(col_names)

    # make empty matrix to store the sums of correlation matrices
    # corr_sums = np.zeros((N_bins, N_bins))

    chi2 = 0

    # Calculate correlation matrix for each l.o.s.
    for ID in ID_list:

        print('Calculating correlation matrix for pointing ', ID)

        # Load normalized counts from 1000 mocks with pandas
        # Each row is a mock, each column is a bin
        counts_filename = counts_dir + 'normed_counts_all_' + ID + '.dat'
        DD = pd.read_csv(counts_filename, sep='\s+', names=col_names)

        # Calculate correlation matrix
        corr = DD.corr().values

        # Invert covariance matrix and save to file
        inv_corr = linalg.inv(corr)

        # load dd counts
        dd_filename = mock_dd_dir + 'dd_' + ID + '.dat'
        dd = np.genfromtxt(dd_filename)

        # load mean normalized dd counts
        sigma_file = sigma_dir + 'stats_' + ID + '.dat'
        dd_mean, std = np.genfromtxt(sigma_file, unpack=True, usecols=[0,2])

        for i in range(N_bins):
            for j in range(N_bins):
                dd_i = dd[i]
                dd_j = dd[j]
                mm_i = dd_mean[i]
                mm_j = dd_mean[j]
                r_ij = inv_corr[i,j]
                sigma_i = std[i]
                sigma_j = std[j]

                chi2 += ( (dd_i - mm_i) * (dd_j-mm_j) * r_ij / (sigma_i*sigma_j) )

    print(chi2)
if __name__ == '__main__':
    main()