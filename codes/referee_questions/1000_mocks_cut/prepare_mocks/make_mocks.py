import numpy as np
import os, sys

#------------------------------------------------------------------------------#
'''
Make N_mocks mocks with the same number of points as are in SEGUE data.
See C code for more details.

Input is such that we can make several mocks simultaneously by opening different
screen sessions and running different bash scripts
'''
#------------------------------------------------------------------------------#

def main():

    elements_needed = int(4)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args   == elements_needed)
    N_stars         = args_array[1]         # Number of stars per temp galaxy
    N_mocks         = int(args_array[2])    # Number of mocks to make
    run_num         = int(args_array[3])    # Which we start at

    # Establish which mocks are to be made
    mock_nums = np.arange(N_mocks) + 1
    mock_nums += N_mocks * run_num

    for i in mock_nums:

        mock_dir = './data/mock_' + str(i) +'/'

        cmd = './bin/make_galaxy ' + N_stars + ' ' + str(i)
        os.system(cmd)

        cmd2 = 'python clean_mocks.py ' + str(i)
        os.system(cmd2)

        cmd3 = 'rm ' + mock_dir + 'temp*'
        os.system(cmd3)

if __name__ == '__main__':
    main()