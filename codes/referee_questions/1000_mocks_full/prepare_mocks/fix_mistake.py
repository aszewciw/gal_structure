# Take mock stars in each line of sight, randomly shuffle them,
# and output exact number as are in each cleaned SEGUE l.o.s.
# Add number of stars as first line in output file

import numpy as np
import sys, os

RAW_DIR = '../../data/'

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

    N_mocks = 1000
    # Load pointing IDs and desired number of stars
    pointing_file = RAW_DIR + 'todo_list.ascii.dat'
    ID, N_stars = np.genfromtxt(pointing_file, skip_header=1, unpack=True,
        dtype=int, usecols=[0, 10])
    N_pointings = len(ID)

    for j in range(N_mocks):

        OUT_DIR = './data/mock_' + str(j+1) + '/'

        # print('On mock %d \n', j+1)
        np.random.seed()

        # Load stars from each l.o.s., shuffle, cut, and output
        for i in range(N_pointings):

            ID_current = str(ID[i])
            N_data = N_stars[i]

            # Load position data for mock stars
            mock_file = OUT_DIR + 'mock_' + ID_current + '.xyz.dat'
            if not os.path.isfile(mock_file):
                sys.stderr.write('Error: ' + mock_file + ' does not exist.\n')
                sys.stderr.write('Remake mock # ' + str(j+1))
            xyz = np.genfromtxt(mock_file, skip_header=1)
            N_mock = len(xyz)

            # delete_me = np.arange(diff)
            # xyz = np.delete(xyz, delete_me, 0)
            # if N_data != len(xyz):
            #     print("Something went wrong! Incorrect number of stars for " + ID_current)
            #     continue

            # Output new data
            out_file = OUT_DIR + 'mock_' + ID_current + '.xyz.dat'
            np.savetxt(out_file, xyz, fmt='%1.6f')

            # Add number of elements as first line in file
            line_prepender(out_file, str(int(N_mock)))

    print('Data cleaned. Mocks completed.\n')

if __name__ == '__main__':
    main()