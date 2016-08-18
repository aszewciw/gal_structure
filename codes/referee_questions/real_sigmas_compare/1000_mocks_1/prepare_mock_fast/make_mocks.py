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
    N_procs         = args_array[3]         # Number of processes to use

    # Establish which mocks are to be made
    mock_nums = np.arange(N_mocks) + 1

    # Make all 1000 mocks
    cmd = 'mpirun -n ' + N_procs + ' ./bin/make_galaxy ' + N_stars + ' ' + str(N_mocks)
    os.system(cmd)

    cmd = 'python clean_mocks.py ' + N_procs + ' ' + str(N_mocks)
    os.system(cmd)

    for i in mock_nums:

        mock_dir = './data/mock_' + str(i) +'/'

        # cmd = 'python clean_mocks.py ' + N_procs + ' ' + str(i)
        # os.system(cmd)

        cmd = 'rm ' + mock_dir + 'proc*'
        os.system(cmd)

if __name__ == '__main__':
    main()