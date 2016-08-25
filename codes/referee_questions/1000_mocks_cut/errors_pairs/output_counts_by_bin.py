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
    input_filename = rawdata_dir + 'todo_list.ascii.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    ID_list = np.genfromtxt(input_filename, skip_header=1, unpack=True, usecols=[0],
                dtype=str)

    print(ID_list)
    N_los = len(ID_list)

    # # Load bins information -- this is made in a separate place
    # bins_file = bins_dir + 'rbins.ascii.dat'
    # if not os.path.isfile(bins_file):
    #     sys.stderr.write('Error: ' + bins_file + ' does not exist.\n')

    # # We really just want the number of bins
    # with open(bins_file) as b:
    #     N_bins = int(b.readline())

    # # Make a dictionary to hold all counts for each bin
    # bin_counts = {}

    # for i in range(N_bins):
    #     tag = 'bin_' + str(i)
    #     bin_counts[tag] = np.zeros((N_mocks, N_los))

    # # loop over each l.o.s.
    # for p in todo_list:

    #     sys.stderr.write(' {}\n'.format(p.ID))

    #     # Load DD counts from all mocks for this pointing
    #     counts_file = data_dir + 'counts_all_' + p.ID + '.dat'
    #     DD = np.genfromtxt(counts_file, dtype=int)

    #     # loop over different bins and add DD to appropriate dictionary
    #     for i in range(N_bins):

    #     # Output data
    #     output_filename = data_dir + 'counts_all_' + p.ID + '.dat'
    #     np.savetxt(output_filename, DD_raw_all, fmt='%d')


if __name__ == '__main__':
    main()