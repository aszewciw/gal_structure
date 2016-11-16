import numpy as np

#-----------------------------------------------------------------------------#
'''
Take mocks, which have unshuffled thin and thick disks upon creation, with more
stars than are in the corresponding line of sight. Shuffle mocks, cut out some
stars to produce files which contain the same number of stars as are in the
corresponding SEGUE l.o.s.
'''
#-----------------------------------------------------------------------------#


DATA_DIR = '../../data/'
OUT_DIR = './data/'

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

    print('Mocks have too many stars. Randomly removing some.\n')
    np.random.seed()

    # Load pointing IDs and desired number of stars
    pointing_file = DATA_DIR + 'todo_list.ascii.dat'
    ID, N_stars = np.genfromtxt(pointing_file, skip_header=1, unpack=True,
        dtype=int, usecols=[0, 10])
    N_pointings = len(ID)

    # Load stars from each l.o.s., shuffle, cut, and output
    for i in range(N_pointings):

        ID_current = str(ID[i])
        N_data = N_stars[i]

        # Load position data for mock stars
        mock_file = OUT_DIR + 'temp_mock_' + ID_current + '.xyzw.dat'
        xyzw = np.genfromtxt(mock_file)

        # Randomly cut from mock sample to make it size of SEGUE data
        N_mock = len(xyzw)
        diff = N_mock - N_data
        if diff < 0:
            print("Oh no! We didn't make enough stars for " + ID_current)
            continue
        delete_me = np.arange(diff)
        np.random.shuffle(xyzw)
        xyzw = np.delete(xyzw, delete_me, 0)
        if N_data != len(xyzw):
            print("Something went wrong! Incorrect number of stars for " + ID_current)
            continue

        # Output new data
        out_file = OUT_DIR + 'mock_' + ID_current + '.xyzw.dat'
        np.savetxt(out_file, xyzw, fmt='%1.6f')

        # Add number of elements as first line in file
        line_prepender(out_file, str(int(N_data)))

    print('Data cleaned. Mocks completed.\n')

if __name__ == '__main__':
    main()