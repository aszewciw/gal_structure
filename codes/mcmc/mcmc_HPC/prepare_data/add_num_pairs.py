
'''
This is pretty dumb too. When doing pair counting, I didn't
add the number of points at the beginning. Going to just
explicitly do this in Python right now because bleh...
'''

import numpy as np
import os, sys, math
import string, csv
import pickle

def main():

    data_dir  = '../data/'
    raw_dir   = data_dir + 'raw/'
    pairs_dir = data_dir + 'model_pairs/'
    todo_file = raw_dir + 'todo_list.ascii.dat'
    ID        = np.genfromtxt(todo_file, unpack=True, usecols=[0], dtype=str)

    bins = np.arange(12)
    bins += 1

    for p in ID:

        for b in bins:
            bin_num = str(b)
            pairs_file = pairs_dir + 'counts_' + p + '.bin_' + bin_num + '.dat'
            i, j = np.genfromtxt(pairs_file, unpack=True)
            N_pairs = len(i)

            outfile = pairs_dir + 'pairs_' + p + '.bin_' + bin_num + '.dat'
            with open(outfile, 'w') as f:
                f.write(str(N_pairs))
                f.write('\n')
                for k in range(N_pairs):
                    f.write("{} {}\n".format(i[k], j[k]))

if __name__ == '__main__':
    main()