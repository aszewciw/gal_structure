import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os

#------------------------------------------------------------------------------#
'''
Produce a correlation matrix plot for each SEGUE l.o.s. using 1000 mocks.
Make a gif from the files.
'''
#------------------------------------------------------------------------------#

rawdata_dir = '../data/'
counts_dir  = '../1000_mocks_cut/errors_pairs/data/'
plots_dir   = './plots/'

#------------------------------------------------------------------------------#
def GIF_MOVIE(files, output_gif, delay=60, repeat=True, removef=False):
    """
    Given a list if 'files', it creates a gif file, and deletes temp files.

    Parameters
    ----------
    files: array_like
            List of abs. paths to temporary figures

    output_gif: str
            Absolute path to output gif file.
    """
    loop = -1 if repeat else 0
    os.system('convert -delay %d -loop %d %s %s' %( delay,loop," ".join(files), \
        output_gif) )

    if removef:
        for fname in files: os.remove(fname)

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

    # Create list of png's for use in making gif
    png_list =[]

    # Calculate correlation matrix for each l.o.s.
    for ID in ID_list:

        # Load counts from 1000 mocks with pandas
        # Each row is a mock, each column is a bin
        counts_filename = counts_dir + 'counts_all_' + ID + '.dat'
        DF = pd.read_csv(counts_filename, sep='\s+', names=col_names)

        # Calculate correlation matrix
        corr = DF.corr()

        # plot heatmap of matrix
        plt.clf()
        sns.set(style="white")
        mask = np.zeros_like(corr, dtype=np.bool)
        mask[np.triu_indices_from(mask)] = True
        f, ax = plt.subplots(figsize=(11, 9))
        cmap = sns.diverging_palette(145, 280, s=85, l=25, n=7, as_cmap=True)
        sns.heatmap(corr, mask=mask, cmap=cmap,square=True, annot=True,
                    xticklabels=col_names, yticklabels=col_names, linewidths=.5,
                    cbar_kws={"shrink": .5}, ax=ax, vmin=-1.0, vmax=1.0)
        plt.title('Correlation Matrix for l.o.s. ' + ID, fontsize=20)
        plt.xlabel('Bin Center (kpc)', fontsize=18)
        plt.ylabel('Bin Center (kpc)', fontsize=18)

        fig_name = plots_dir + 'corr_matrix_' + ID + '.png'
        plt.savefig(fig_name)
        png_list.append(fig_name)

    gif_name = plots_dir + 'corr_matrix.gif'
    GIF_MOVIE(png_list, gif_name)

if __name__ == '__main__':
    main()