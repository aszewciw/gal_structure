import pandas as pd
from config import *
from scipy import linalg

#------------------------------------------------------------------------------#
'''
For each SEGUE l.o.s., load the raw pair counts from 1000 mocks in each of 12
radial bins.

Calculate the inverse correlation matrix and output file
'''
#------------------------------------------------------------------------------#

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

        out_file = errors_dir + 'correlation_' + ID + '.dat'
        np.savetxt(out_file, cov, fmt='%.6e')

        out_file = errors_dir + 'inv_correlation_' + ID + '.dat'
        np.savetxt(out_file, inv_cov, fmt='%.6e')

if __name__ == '__main__':
    main()