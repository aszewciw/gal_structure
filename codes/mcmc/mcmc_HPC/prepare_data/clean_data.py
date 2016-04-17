
'''
As I'm working on this HPC project, I want to clean some
files so I have the following things:

1. Files containing just Z, R, W, for uniform points
2. Files containing just raw DD counts
3. Files containing just the fractional errors

There is no need to overload my data structures with
things I'll never use in the MCMC.
This is a bit sloppy of a way to do this all, but for now
my main concern is getting my mcmc to work. After that, I
will work on data preparation files.
'''

import numpy as np
import os, sys, math
import string, csv
import pickle

def main():

    data_dir  = '../data/'
    raw_dir   = data_dir + 'raw/'
    dd_dir    = data_dir + 'dd/'
    err_dir   = data_dir + 'errors/'
    model_dir = data_dir + 'model_positions/'

    todo_file = raw_dir + 'todo_list.ascii.dat'
    ID        = np.genfromtxt(todo_file, unpack=True, skip_header=1,
        usecols=[0], dtype=str)

    # Repack file of just pointing IDs
    outfile   = '../data/raw/pointing_ID.dat'
    with open(outfile, 'w') as f:
        for i in range(len(ID)):
            f.write("{}\n".format(ID[i]))


    for p in ID:

        # Repack file containing normalized DD only
        dd_file = dd_dir + 'DD_' + p + '.dat'
        dd      = np.genfromtxt(dd_file, usecols=[2])
        outfile = dd_dir + 'dd_' + p + '.dat'
        np.savetxt(outfile, dd)

        # Repack file containing Z, R, and W=1.0 only
        ZRW_file = model_dir + 'uniform_' + p + '.ascii.dat'
        Z, R, W  = np.genfromtxt(ZRW_file, unpack=True, skip_header=1,
            usecols=[5, 6, 10], dtype=None)
        N_points = len(Z)
        outfile  = model_dir + 'uniform_ZRW_' + p + '.dat'
        with open(outfile, 'w') as f:
            f.write(str(N_points))
            f.write('\n')
            for i in range(N_points):
                f.write("{} {} {}\n".format(
                    str(Z[i]), str(R[i]), str(W[i])))

        # Repack uniform error files
        uni_jk_file = err_dir + 'uniform_' + p + '_jk_error.dat'
        uni_jk_err  = np.genfromtxt(uni_jk_file, unpack=True, usecols=[7])
        outfile     = err_dir + 'uniform_' + p + '_frac_error.dat'
        np.savetxt(outfile, uni_jk_err)

        # Repack data error files
        dat_jk_file = err_dir + 'star_' + p + '_jk_error.dat'
        dat_jk_err  = np.genfromtxt(dat_jk_file, unpack=True, usecols=[7])
        outfile     = err_dir + 'star_' + p + '_frac_error.dat'
        np.savetxt(outfile, dat_jk_err)

if __name__ == '__main__':
    main()
