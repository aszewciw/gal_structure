import numpy as np
import pandas as pd
import sys
import PIL.Image
sys.modules['Image'] = PIL.Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams.update({'figure.max_open_warning': 0})
import os

#------------------------------------------------------------------------------#
'''
Produce a correlation matrix plot for each SEGUE l.o.s. using 1000 mocks.
Make a gif from the files.
'''
#------------------------------------------------------------------------------#

rawdata_dir = '../../data/'
rbins_dir   = '../../mcmc_mock/data/rbins/'
mod0_dir    = '../../1000_mocks_cut/errors_pairs/data/'
mod1_dir    = '../1000_mocks_1/errors_pairs/data/'
mod2_dir    = '../1000_mocks_2/errors_pairs/data/'
plots_dir   = '../plots/'

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

    # Create list of png's for use in making gif
    png_list_0 =[]
    png_list_1 =[]
    png_list_2 =[]

    # Calculate covariance matrix for each l.o.s.
    for ID in ID_list:

        # Load counts from 1000 mocks with pandas
        # Each row is a mock, each column is a bin

        # Load fiducial
        mod0_filename = mod0_dir + 'normed_counts_all_' + ID + '.dat'
        DF_0 = pd.read_csv(mod0_filename, sep='\s+')

        # Calculate fiducial covariance
        cov_0 = DF_0.corr()

        # Load model 1
        mod1_filename = mod1_dir + 'normed_counts_all_' + ID + '.dat'
        DF_1 = pd.read_csv(mod1_filename, sep='\s+')

        # Calculate fiducial covariance
        cov_1 = DF_1.corr()

        # Load model 2
        mod2_filename = mod2_dir + 'normed_counts_all_' + ID + '.dat'
        DF_2 = pd.read_csv(mod2_filename, sep='\s+')

        # Calculate model 2 covariance
        cov_2 = DF_2.corr()

        # plot first heatmap
        plt.clf()
        sns.set(style="white")
        mask = np.zeros_like(cov_0, dtype=np.bool)
        mask[np.triu_indices_from(mask,1)] = True
        f, ax = plt.subplots(figsize=(11, 9))
        cmap = sns.diverging_palette(145, 280, s=85, l=25, n=7, as_cmap=True)
        sns.heatmap(cov_0, mask=mask, cmap=cmap,square=True, annot=True,
                    xticklabels=col_names, yticklabels=col_names, linewidths=.5,
                    cbar_kws={"shrink": .5}, ax=ax, vmin=-2.0, vmax=2.0)
        plt.title('Covariance matrix for l.o.s. ' + ID, fontsize=20)
        plt.xlabel('Bin Center (kpc)', fontsize=18)
        plt.ylabel('Bin Center (kpc)', fontsize=18)
        fig_name = plots_dir + 'cov0_' + ID + '.png'
        plt.savefig(fig_name)
        png_list_0.append(fig_name)

        # plot second heatmap
        plt.clf()
        sns.set(style="white")
        mask = np.zeros_like(cov_1, dtype=np.bool)
        mask[np.triu_indices_from(mask,1)] = True
        f, ax = plt.subplots(figsize=(11, 9))
        cmap = sns.diverging_palette(145, 280, s=85, l=25, n=7, as_cmap=True)
        sns.heatmap(cov_1, mask=mask, cmap=cmap,square=True, annot=True,
                    xticklabels=col_names, yticklabels=col_names, linewidths=.5,
                    cbar_kws={"shrink": .5}, ax=ax, vmin=-2.0, vmax=2.0)
        plt.title('Covariance matrix for l.o.s. ' + ID, fontsize=20)
        plt.xlabel('Bin Center (kpc)', fontsize=18)
        plt.ylabel('Bin Center (kpc)', fontsize=18)
        fig_name = plots_dir + 'cov1_' + ID + '.png'
        plt.savefig(fig_name)
        png_list_1.append(fig_name)

        # plot heatmap of matrix
        plt.clf()
        sns.set(style="white")
        mask = np.zeros_like(cov_2, dtype=np.bool)
        mask[np.triu_indices_from(mask,1)] = True
        f, ax = plt.subplots(figsize=(11, 9))
        cmap = sns.diverging_palette(145, 280, s=85, l=25, n=7, as_cmap=True)
        sns.heatmap(cov_2, mask=mask, cmap=cmap,square=True, annot=True,
                    xticklabels=col_names, yticklabels=col_names, linewidths=.5,
                    cbar_kws={"shrink": .5}, ax=ax, vmin=-2.0, vmax=2.0)
        plt.title('Covariance matrix for l.o.s. ' + ID, fontsize=20)
        plt.xlabel('Bin Center (kpc)', fontsize=18)
        plt.ylabel('Bin Center (kpc)', fontsize=18)
        fig_name = plots_dir + 'cov2_' + ID + '.png'
        plt.savefig(fig_name)
        png_list_2.append(fig_name)

    print("Plots finished. Making gifs...\n")
    gif_name = plots_dir + 'cov0.gif'
    GIF_MOVIE(png_list_0, gif_name,removef=True)
    gif_name = plots_dir + 'cov1.gif'
    GIF_MOVIE(png_list_1, gif_name,removef=True)
    gif_name = plots_dir + 'cov2.gif'
    GIF_MOVIE(png_list_2, gif_name,removef=True)

if __name__ == '__main__':
    main()