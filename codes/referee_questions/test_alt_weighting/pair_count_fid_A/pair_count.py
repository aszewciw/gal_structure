'''
Loops over all SEGUE los and produces a file for each
mock containing the normalized dd counts.
'''

from config import *
import os, sys
import numpy as np


def main():

    # # CL Input
    # # star_factor = N_random / N_data in each l.o.s.
    # elements_needed = int(2)
    # args_array      = np.array(sys.argv)
    # N_args          = len(args_array)
    # assert(N_args == elements_needed)
    # star_factor     = args_array[1]

    todo_file = rawdata_dir + 'todo_list.ascii.dat'
    ID_list = np.genfromtxt(todo_file, skip_header=1, usecols=[0], unpack=True,
                            dtype=str)
    N_los = len(ID_list)

    bins_file = data_dir + 'rbins.ascii.dat'
    if not os.path.isfile(bins_file):
        sys.stderr.write('Error: ' + bins_file + ' does not exist.\n')

    for p in ID_list:

        # A
        in_file = data_dir + 'nonuni_reweighted_A_' + p + '.xyzw.dat'

        if not os.path.isfile(in_file):
            sys.stderr.write('Error: ' + in_file + ' does not exist.\n')
            continue

        output_file = data_dir + 'mm_A_' + p + '.dat'

        cmd = ( './pair_count ' + in_file + ' ' + bins_file
            + ' > ' + output_file )
        os.system(cmd)


        # B
        in_file = data_dir + 'nonuni_reweighted_B_' + p + '.xyzw.dat'

        if not os.path.isfile(in_file):
            sys.stderr.write('Error: ' + in_file + ' does not exist.\n')
            continue

        output_file = data_dir + 'mm_B_' + p + '.dat'

        cmd = ( './pair_count ' + in_file + ' ' + bins_file
            + ' > ' + output_file )
        os.system(cmd)


        # C
        in_file = data_dir + 'nonuni_reweighted_C_' + p + '.xyzw.dat'

        if not os.path.isfile(in_file):
            sys.stderr.write('Error: ' + in_file + ' does not exist.\n')
            continue

        output_file = data_dir + 'mm_C_' + p + '.dat'

        cmd = ( './pair_count ' + in_file + ' ' + bins_file
            + ' > ' + output_file )
        os.system(cmd)

if __name__ == '__main__':
    main()