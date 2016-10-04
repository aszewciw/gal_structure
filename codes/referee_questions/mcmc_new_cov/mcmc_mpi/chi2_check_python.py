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

    # Initialize different chi2 calculations
    chi2_tt = 0
    chi2_te = 0
    chi2_et = 0
    chi2_ee = 0
    chi2_tt_cov = 0
    chi2_te_cov = 0
    chi2_et_cov = 0
    chi2_ee_cov = 0

    # Count instances where dd=0 and total number of data points
    zero_counts = 0
    all_counts = 0

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

        # load fractional sigmas
        err_file = errors_dir + 'frac_error_' + ID + '.dat'
        std_frac = np.genfromtxt(err_file)

        # load counts from weighted randoms
        mm_filename = './data/mm_' + ID + '.dat'
        mm_weighted = np.genfromtxt(mm_filename)

        # Calculate chi2 using a number of different methods
        for i in range(N_bins):

            for j in range(N_bins):

                # Data points from this mock
                data_i = dd[i]
                data_j = dd[j]

                # Means from 1000 mocks
                model_true_i = dd_mean[i]
                model_true_j = dd_mean[j]

                # Weighted random approximation to mean
                model_est_i = mm_weighted[i]
                model_est_j = mm_weighted[j]

                # Inverse correlation matrix element
                r_ij = inv_corr[i,j]

                # Actual standard deviations from 1000 mocks
                std_true_i = std[i]
                std_true_j = std[j]

                # Estimated standard deviations from 1000 mocks
                std_est_i = std_frac[i]*model_est_i
                std_est_j = std_frac[j]*model_est_j

                # Use true means and true std
                chi2_tt_cov += ( (data_i-model_true_i) * (data_j-model_true_j) * r_ij
                    / (std_true_i*std_true_j) )

                # Use true means and estimated std
                chi2_te_cov += ( (data_i-model_true_i) * (data_j-model_true_j) * r_ij
                    / (std_est_i*std_est_j) )

                # Use weighted random mm and true std
                chi2_et_cov += ( (data_i-model_est_i) * (data_j-model_est_j) * r_ij
                    / (std_true_i*std_true_j) )

                # Use weighted random mm and estimated std
                chi2_ee_cov += ( (data_i-model_est_i) * (data_j-model_est_j) * r_ij
                    / (std_est_i*std_est_j) )

                # Do non-covariance calculations as well
                if(i==j):
                    # first update counts
                    all_counts +=1

                    if data_i==0.0:
                        zero_counts +=1

                    chi2_tt += ((data_i-model_true_i)/std_true_i)**2
                    chi2_te += ((data_i-model_true_i)/std_est_i)**2
                    chi2_et += ((data_i-model_est_i)/std_true_i)**2
                    chi2_ee += ((data_i-model_est_i)/std_est_i)**2


    print('\nResults of chi-squared measurements for diffferent instances:\n')
    print('Using true mean and true stdev:')
    print('     Without covariance: {}, With covariance: {}'.format(chi2_tt, chi2_tt_cov))
    print('Using true mean and estimated stdev:')
    print('     Without covariance: {}, With covariance: {}'.format(chi2_te, chi2_te_cov))
    print('Using estimated mean and true stdev:')
    print('     Without covariance: {}, With covariance: {}'.format(chi2_et, chi2_et_cov))
    print('Using estimate mean and estimated stdev:')
    print('     Without covariance: {}, With covariance: {}'.format(chi2_ee, chi2_ee_cov))
    print('\nThere were {}/{} values of dd=0 for this mock.'.format(zero_counts,all_counts))

if __name__ == '__main__':
    main()