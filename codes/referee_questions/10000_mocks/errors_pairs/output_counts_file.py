from config import *

'''
output file containing all raw pair counts for use in pandas calculation of
covariance matrix

each column is a bin, each row is a mock
'''

# ---------------------------------------------------------------------------- #

def main():

    # Read in number of mocks
    # elements_needed = int(2)
    # args_array      = np.array(sys.argv)
    # N_args          = len(args_array)
    # assert(N_args   == elements_needed)
    # N_mocks         = int(args_array[1])
    N_mocks = 1000

    # Load list of pointings
    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    # Load bins information -- this is made in a separate place
    bins_file = bins_dir + 'rbins.ascii.dat'
    if not os.path.isfile(bins_file):
        sys.stderr.write('Error: ' + bins_file + ' does not exist.\n')

    # We really just want the number of bins
    with open(bins_file) as b:
        N_bins = int(b.readline())

    # loop over each l.o.s.
    for p in todo_list:

        sys.stderr.write('Calculating stats for pointing {}\n'.format(p.ID))

        # Empty arrays where each row is counts for 1 mock in current l.o.s.
        DD_raw_all = np.zeros((N_mocks, N_bins))
        # DD_all     = np.zeros((N_mocks, N_bins))

        # loop over all mocks
        for i in range(N_mocks):

            # Load counts for a single mock
            corr_file = ( data_dir + 'mock_' + str(i+1) + '/mock_pairs_'
                        + p.ID + '.dat' )
            # DD_raw_all[i], DD_all[i] = np.genfromtxt( corr_file, unpack=True,
            #                             usecols=[4, 5] )
            DD_raw_all[i] = np.genfromtxt( corr_file, dtype=int, unpack=True,
                                        usecols=[4] )

        # Output data
        output_filename = data_dir + 'counts_all_' + p.ID + '.dat'
        np.savetxt(output_filename, DD_raw_all, fmt='%d')


if __name__ == '__main__':
    main()