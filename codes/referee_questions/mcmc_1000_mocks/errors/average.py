from config import *

def main():
    # Read in number of mocks
    elements_needed = int(2)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args   == elements_needed)
    N_mocks         = int(args_array[1])

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

        sys.stderr.write('Calculating stats for pointing{}\n'.format(p.ID))

        # Empty arrays where each row is counts for 1 mock in current l.o.s.
        DD_raw_all = np.zeros((N_mocks, N_bins))
        DD_all     = np.zeros((N_mocks, N_bins))

        # loop over all mocks
        for i in range(N_mocks):

            # Load counts for a single mock
            corr_file = ( mock_dir + 'mock_' + str(i+1) + '/mock_pairs_'
                + p.ID + '.dat' )
            DD_raw_all[i], DD_raw[i] = np.genfromtxt( corr_file, unpack=True,
                usecols=[4, 5] )


        # Find mean across all mocks
        DD_raw_mean = np.sum(DD_raw_all, axis=0) / N_mocks
        DD_mean     = np.sum(DD_all, axis=0) / N_mocks

        # Find variance and stdev
        DD_raw_diff_sq = ( DD_raw_all - DD_raw_mean )**2
        DD_diff_sq     = ( DD_all - DD_mean )**2
        DD_raw_var = np.sum(DD_raw_diff_sq, axis=0) / N_mocks
        DD_var     = np.sum(DD_diff_sq, axis=0) / N_mocks
        DD_raw_std = np.sqrt(DD_raw_var)
        DD_std     = np.sqrt(DD_var)

        # Output data
        output_filename = stats_dir + 'stats_' + p.ID + '.dat'
        output_file     = open(output_filename, 'w')

        for i in range(N_bins):
            output_file.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                DD_mean[i], DD_var[i], DD_std[i],
                DD_raw_mean[i], DD_raw_var[i], DD_raw_std[i] ) )

        output_file.close()

if __name__ == '__main__':
    main()