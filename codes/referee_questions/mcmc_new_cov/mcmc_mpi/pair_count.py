'''
Loops over all SEGUE los and produces a file for each
mock containing the normalized dd counts.
'''

# from config import *
import os, sys
import numpy as np

rawdata_dir = '../../data/'
rbins_dir = '../data/rbins/'
mwm_dir = './data/'

def main():

    input_filename = rawdata_dir + 'todo_list.ascii.dat'
    ID_list = np.genfromtxt(todo_file, skip_header=1, usecols=[0], unpack=True,
                            dtype=str)
    N_los = len(ID_list)

    bins_file = rbins_dir + 'rbins.ascii.dat'
    if not os.path.isfile(bins_file):
        sys.stderr.write('Error: ' + bins_file + ' does not exist.\n')

    for p in ID_list:

        in_file = mwm_dir + 'MWM_' + p + '.xyzw.dat'

        if not os.path.isfile(in_file):
            sys.stderr.write('Error: ' + in_file + ' does not exist.\n')
            continue

        output_file = mwm_dir + 'mm_' + p + '.dat'

        cmd = ( './pair_count ' + in_file + ' ' + bins_file
            + ' > ' + output_file )
        os.system(cmd)

if __name__ == '__main__':
    main()