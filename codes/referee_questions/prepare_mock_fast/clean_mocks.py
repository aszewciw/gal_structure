import numpy as np
import os, sys

#-----------------------------------------------------------------------------#
'''
Take mocks, which have unshuffled thin and thick disks upon creation, with more
stars than are in the corresponding line of sight. Shuffle mocks, cut out some
stars to produce files which contain the same number of stars as are in the
corresponding SEGUE l.o.s.
'''
#-----------------------------------------------------------------------------#


DATA_DIR = '../data/'
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

    # Read in number of procs used in making mocks
    elements_needed = int(2)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args   == elements_needed)
    N_procs         = int(args_array[1])

    # Make array of process IDs
    proc_IDs = np.arange(N_procs)

    print('Merging files from all {} processes.\n'.format(N_procs))
    np.random.seed()

    # Load pointing IDs and desired number of stars
    pointing_file = DATA_DIR + 'todo_list.ascii.dat'
    ID, N_stars = np.genfromtxt(pointing_file, skip_header=1, unpack=True,
        dtype=int, usecols=[0, 10])
    N_pointings = len(ID)

    # Load stars from each l.o.s., shuffle, cut, and output
    for i in range(N_pointings):

        # if(ID[i]%10==0):
        print('On pointing number {}\n'.format(ID[i]))

        # Get info for current pointing
        ID_current = str(ID[i])
        N_data = N_stars[i]

        # Shuffle IDs so we read files from random procs
        np.random.shuffle(proc_IDs)

        # Make array of zeros to be filled by data from each file
        xyz = np.zeros((N_data, 3))

        # Counter to check which index we're starting from
        start_ind = 0

        # Loop over files from different processes
        for PID in proc_IDs:

            print('Checking process number ' + PID + '\n')

            # Check if we have enough stars for this pointing
            if start_ind==N_data:
                break
            elif start_ind>N_data:
                sys.stderr.write('Error: we exceeded the number of desired stars\n')
                sys.exit()

            # Check if file exists for this process and load
            mock_file = ( OUT_DIR + 'proc_' + str(PID) + '_mock_' + ID_current
                + '.xyz.dat' )
            if not os.path.isfile(mock_file):
                continue
            xyz_tmp = np.genfromtxt(mock_file)
            np.random.shuffle(xyz_tmp)

            # Get number of stars in this file
            N_tmp = len(xyz_tmp)

            # Find the segment of xyz to which we are adding this piece
            end_ind = start_ind + N_tmp

            # Check if we're past the end of the array
            if end_ind > N_data:

                # Cut elements from temporary array
                N_cut = end_ind - N_data
                xyz_tmp = xyz_tmp[N_cut:]

                # Reassign ending index
                end_ind = N_data

            # Assign these stars to main array
            xyz[start_ind:end_ind] = xyz_tmp

            # Add to counter how many stars we've assigned
            start_ind = end_ind

        # Shuffle finished pointing array and output to file
        np.random.shuffle(xyz)
        out_file = OUT_DIR + 'mock_' + ID_current + '.xyz.dat'
        np.savetxt(out_file, xyz, fmt='%1.6f')

        # Add number of elements as first line in file
        line_prepender(out_file, str(int(N_data)))

    print('Data cleaned. Mocks completed.\n')

if __name__ == '__main__':
    main()