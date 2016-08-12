import pandas as pd
from config import *

#------------------------------------------------------------------------------#
'''
For each SEGUE l.o.s., load the raw pair counts from 1000 mocks in each of 12
radial bins.

Calculate the covariance matrix. Output a file.
'''
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

    # make empty matrix to store the sums of correlation matrices
    # corr_sums = np.zeros((N_bins, N_bins))

    # Calculate correlation matrix for each l.o.s.
    for ID in ID_list:

        print('Calculating covariance for pointing ', ID)

        # Load normalized counts from 1000 mocks with pandas
        # Each row is a mock, each column is a bin
        counts_filename = mocks_1000_dir + 'normed_counts_all_' + ID + '.dat'
        DD = pd.read_csv(counts_filename, sep='\s+', names=col_names)

        # Load RR counts
        RR_file = rr_dir + 'uniform_rr_' + ID + '.dat'
        RR = np.genfromtxt(RR_file)

        # Calculate DD/RR
        DD_RR = DD/RR

        # Calculate covariance matrix
        cov = DD_RR.cov()

        # Save to a file
        out_file = errors_dir + 'covariance_' + ID + '.dat'
        np.savetxt(out_file, cov.values)

        # Add to dictionary
        # corr_dict[ID] = corr.values

        # Add to correlation sum
        # corr_sums += np.nan_to_num(corr.values)

    # # compute the average correlation matrix value
    # corr_ave = corr_sums / N_los

    # # plot heatmap of matrix
    # sns.set(style="white")
    # mask = np.zeros_like(corr_ave, dtype=np.bool)
    # mask[np.triu_indices_from(mask)] = True
    # f, ax = plt.subplots(figsize=(11, 9))
    # cmap = sns.diverging_palette(145, 280, s=85, l=25, n=7, as_cmap=True)
    # sns.heatmap(corr_ave, mask=mask, cmap=cmap,square=True, annot=True,
    #             xticklabels=col_names, yticklabels=col_names, linewidths=.5,
    #             cbar_kws={"shrink": .5}, ax=ax)
    # plt.title('Average Correlation Matrix Across l.o.s. (1000 mocks)', fontsize=20)
    # plt.xlabel('Bin Center (kpc)', fontsize=18)
    # plt.ylabel('Bin Center (kpc)', fontsize=18)

    # fig_name = plots_dir + '1000_mocks_corr_matrix.png'
    # plt.savefig(fig_name)

if __name__ == '__main__':
    main()