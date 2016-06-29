# Take mock stars in each line of sight, randomly shuffle them,
# and output exact number as are in each cleaned SEGUE l.o.s.
# Add number of stars as first line in output file

import numpy as np

DATA_DIR = '../data/'

## ------------------------------------------------------------------------- ##

def line_prepender(filename, line):
    '''
    Appends a line to the beginning of a file.

    Arguments:
    1. filename : (str) name of file
    2. line : (str) line to be appended
    '''
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

## ------------------------------------------------------------------------- ##

def main():

    print('Randomly shuffling stars.\n')
    np.random.seed()

    # Load pointing IDs and desired number of stars
    pointing_file = DATA_DIR + 'corr_list.ascii.dat'
    ID, N_stars = np.genfromtxt(pointing_file, skip_header=1, unpack=True,
        dtype=int, usecols=[0, 10])
    N_pointings = len(ID)

    # Load stars from each l.o.s., shuffle, cut, and output
    for i in range(N_pointings):

        ID_current = str(ID[i])
        N_data = N_stars[i]

        # Load position data for mock stars
        mock_file = DATA_DIR + 'temp_mock_' + ID_current + '.xyz.dat'
        xyz = np.genfromtxt(mock_file)

        # Randomly shuffle disks
        N_mock = len(xyz)

        np.random.shuffle(xyz)

        # Output new data
        out_file = DATA_DIR + 'mock_full_' + ID_current + '.xyz.dat'
        np.savetxt(out_file, xyz, fmt='%1.6f')

        # Add number of elements as first line in file
        line_prepender(out_file, str(int(N_mock)))

    print('Data cleaned. Mocks completed.\n')

if __name__ == '__main__':
    main()