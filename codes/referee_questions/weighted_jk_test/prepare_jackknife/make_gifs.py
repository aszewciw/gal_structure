import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os

#------------------------------------------------------------------------------#
'''
Produce a correlation matrix plot for each SEGUE l.o.s. using 1000 mocks.
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

    # Create list of png's for use in making gif
    png_list =[]

    # Calculate correlation matrix for each l.o.s.
    for ID in ID_list:

        fig_name = plots_dir + 'corr_matrix_' + ID + '.png'
        png_list.append(fig_name)

    gif_name = plots_dir + 'corr_matrix.gif'
    GIF_MOVIE(png_list, gif_name)

if __name__ == '__main__':
    main()