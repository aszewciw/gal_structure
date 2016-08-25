import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
plt.rc('text', usetex=True)

#------------------------------------------------------------------------------#
'''
For each SEGUE l.o.s., load the normalized pair counts from 1000 mocks in each
of 12 radial bins.

Calculate the correlation matrix.

Average the correlations across all lines of sight, and plot the averages.

Additional task:
Plot the average and standard deviation of the correlation values across all
l.o.s. on the same plot.
'''
#------------------------------------------------------------------------------#

rawdata_dir = '../data/'
counts_dir  = '../1000_mocks_cut/errors_pairs/data/'
plots_dir   = './plots/'

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
    bin_names = []

    for i in range(N_bins):
        name = str(i)
        bin_names.append(name)

    # Make list store all dataframes of counts
    counts_list = []

    # make empty matrix to store the sums of correlation matrices
    # corr_sums = np.zeros((N_bins, N_bins))

    # Calculate correlation matrix for each l.o.s.
    for ID in ID_list:

        # Set a limit for now
        ID_limit = 200
        ID_value = int(ID)
        if ID_value>ID_limit:
            continue

        # Load counts from 1000 mocks with pandas
        # Each row is a mock, each column is a bin
        counts_filename = counts_dir + 'normed_counts_all_' + ID + '.dat'
        col_names = []
        for i in bin_names:
            col_names.append('p' + ID + 'b' + i)
        DF = pd.read_csv(counts_filename, sep='\s+', names=col_names)

        # Append dataframe to dataframe list
        counts_list.append(DF)


    # concatenate all data frames in list
    COUNTS = pd.concat(counts_list, axis=1)

    corr = COUNTS.corr()

    # print(corr)

    # plot heatmap of matrix
    sns.set(style="white")
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    f, ax = plt.subplots(figsize=(11, 9))
    cmap = sns.diverging_palette(145, 280, s=85, l=25, n=7, as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap=cmap,square=True, fmt='.2f',
                annot=False, annot_kws={'fontsize':5},
                linewidths=0, xticklabels=False, yticklabels=False,
                cbar_kws={"shrink": .5}, ax=ax)
    # plt.title('Correlation matrix for some los', fontsize=20)
    # plt.xlabel('los, bin', fontsize=18)
    # plt.ylabel('los, bin', fontsize=18)

    fig_name = plots_dir + 'corr_matrix_los_bin_all.png'
    # plt.savefig(fig_name, format='pdf')
    plt.savefig(fig_name)

if __name__ == '__main__':
    main()