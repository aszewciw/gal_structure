'''
Loops over all SEGUE los and produces a file for each
mock containing the normalized dd counts.
'''

from config import *
import os, sys
import numpy as np


def main():

    todo_file = rawdata_dir + 'todo_list.ascii.dat'
    ID_list = np.genfromtxt(todo_file, skip_header=1, usecols=[0], unpack=True,
                            dtype=str)
    N_los = len(ID_list)

    bins_file = data_dir + 'rbins.ascii.dat'
    if not os.path.isfile(bins_file):
        sys.stderr.write('Error: ' + bins_file + ' does not exist.\n')

    for p in ID_list:

        in_file = mock_dir + 'mock_' + p + '.xyzw.dat'

        if not os.path.isfile(in_file):
            sys.stderr.write('Error: ' + in_file + ' does not exist.\n')
            continue

        output_file = data_dir + 'mod_mm_' + p + '.dat'

        cmd = ( './pair_count ' + in_file + ' ' + bins_file
            + ' > ' + output_file )
        os.system(cmd)


if __name__ == '__main__':
    main()