

# Take mock stars in each line of sight, randomly shuffle them,
# and output exact number as are in each cleaned SEGUE l.o.s.

import numpy as np
# import os, sys

DATA_DIR = '../data/'

def main():

    print('Mocks have too many stars. Randomly removing some.\n')
    np.random.seed()

    # Load pointing IDs and desired number of stars
    pointing_file = DATA_DIR + 'todo_list.ascii.dat'
    ID, N_stars = np.genfromtxt(pointing_file, skip_header=1, unpack=True, dtype=int, usecols=[0, 10])
    N_pointings = len(ID)

    # Load stars from each l.o.s., shuffle, cut, and output
    for i in range(N_pointings):

        ID_current = str(ID[i])
        N_data = N_stars[i]

        # Load position data for mock stars
        mock_file = DATA_DIR + 'mock_' + ID_current + '.xyz.dat'
        xyz = np.genfromtxt(mock_file)

        # Randomly cut from mock sample to make it size of SEGUE data
        N_mock = len(xyz)
        diff = N_mock - N_data
        if diff < 0:
            print("Oh no! We didn't make enough stars!")
            continue
        delete_me = np.arange(diff)
        np.random.shuffle(xyz)
        xyz = np.delete(xyz, delete_me, 0)

        # Output new data
        out_file = DATA_DIR + 'segue_mock_' + ID_current + '.xyz.dat'
        np.savetxt(out_file, xyz, fmt='%1.6f')

    print('Data cleaned. Mocks completed.\n')

if __name__ == '__main__':
    main()