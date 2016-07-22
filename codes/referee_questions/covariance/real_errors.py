import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------#
'''
For each SEGUE l.o.s., load the raw pair counts from 1000 mocks in each of 12
radial bins.

Calculate the correlation matrix.

Average the correlations across all lines of sight, and plot the averages.

Additional task:
Plot the average and standard deviation of the correlation values across all
l.o.s. on the same plot.
'''
#------------------------------------------------------------------------------#

rawdata_dir = '../data/'
counts_dir  = '../1000_mocks_cut/errors_pairs/data/'

#------------------------------------------------------------------------------#

def main():

    # Load list of pointing IDs
    todo_file = rawdata_dir + 'todo_list.ascii.dat'
    ID_list   = np.genfromtxt(todo_file, skip_header=1, usecols=[0], unpack=True,
                            dtype=str)
    N_los = len(ID_list)

    # Load bins centers
    bins_file   = 'rbins.ascii.dat'
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

    # Make dictionary to store all correlation matrices
    # This is only useful if I want to compute standard deviations
    # corr_dict = {}

    # make empty matrix to store the sums of correlation matrices
    corr_sums = np.zeros((N_bins, N_bins))

    # Calculate correlation matrix for each l.o.s.
    for ID in ID_list:

        # Load counts from 1000 mocks with pandas
        # Each row is a mock, each column is a bin
        counts_filename = counts_dir + 'counts_all_' + ID + '.dat'
        DF = pd.read_csv(counts_filename, sep='\s+', names=col_names)

        # Calculate correlation matrix
        corr = DF.corr()

        # Add to dictionary
        # corr_dict[ID] = corr.values

        # Add to correlation sum
        corr_sums += corr.values

    # compute the average correlation matrix value
    corr_ave = corr_sums / N_los

    # plot heatmap of matrix
    sns.set(style="white")
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    f, ax = plt.subplots(figsize=(11, 9))
    # cmap = sns.diverging_palette(220, 10, as_cmap=True)
    cmap = sns.diverging_palette(145, 280, s=85, l=25, n=7, as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap=cmap,square=True, annot=True,
                 linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)
    plt.title('Average Correlation Matrix Across l.o.s. (1000 mocks)', fontsize=20)
    plt.xlabel('Bin Center (kpc)', fontsize=18)
    plt.ylabel('Bin Center (kpc)', fontsize=18)

    plt.savefig('1000_mocks_corr_matrix.png')

if __name__ == '__main__':
    main()