import numpy as np
import math
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
def gal_weights(Z, R):
    '''
    Returns a weight based on a particular model of the MW.
    For now we will use a two-disk model with the form below.
    This can be expanded at a later time.

    Z - Height above/below galactic plane
    R - Distance from galactic center

    '''

    # Parameters
    thick_s_height = 0.674
    thick_s_length = 2.51
    thin_s_height = 0.233
    thin_s_length = 2.34
    a = 0.1


    weight = ( ( ( math.cosh(Z / 2 / thin_s_height) ) ** (-2) )
        * math.exp(-R / thin_s_length) +
        a * ( ( math.cosh(Z / 2 / thick_s_height) ) ** (-2) )
        * math.exp(-R / thick_s_length))

    return weight

#--------------------------------------------------------------------------

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
        mock_file = OUT_DIR + 'temp_mock_' + ID_current + '.xyzZR.dat'
        xyzZR = np.genfromtxt(mock_file)

        # Randomly cut from mock sample to make it size of SEGUE data
        N_mock = len(xyzZR)
        diff = N_mock - N_data*10
        if diff < 0:
            print("Oh no! We didn't make enough stars for " + ID_current)
            continue
        delete_me = np.arange(diff)
        np.random.shuffle(xyzZR)
        xyzZR = np.delete(xyzZR, delete_me, 0)
        if N_data*10 != len(xyzZR):
            print("Something went wrong! Incorrect number of stars for " + ID_current)
            continue

        # Output file containing xyz and weight
        xyzw_filename = OUT_DIR + 'nonuniform_' + ID_current + '.xyzw.dat'
        xyzw_file = open(xyzw_filename, "w")
        # first output the total number of points
        xyzw_file.write('{}\n'.format(len(xyzZR)))

        # Output file containing xyz and weight
        zrw_filename = OUT_DIR + 'nonuniform_' + ID_current + '.zrw.dat'
        zrw_file = open(zrw_filename, "w")
        # first output the total number of points
        zrw_file.write('{}\n'.format(len(xyzZR)))

        for i in range(len(xyzZR)):

            # Calculate weight based on Z, R
            x = xyzZR[i, 0]
            y = xyzZR[i, 1]
            z = xyzZR[i, 2]
            Z = xyzZR[i, 3]
            R = xyzZR[i, 4]
            weight = gal_weights(Z,R)
            xyzw_file.write('{0:.6e}\t{1:.6e}\t{2:.6e}\t{3:.6e}\n'
                              .format(x, y, z, weight))
            zrw_file.write('{0:.6e}\t{1:.6e}\t{2:.6e}\n'
                              .format(Z, R, weight))
        xyzw_file.close()
        zrw_file.close()

    print('Data cleaned. Mocks completed.\n')

if __name__ == '__main__':
    main()