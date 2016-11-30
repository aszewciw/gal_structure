from config import *
import pandas as pd

'''
output file containing all normalized pair counts for use in pandas calculation
of covariance matrix

each column is a bin, each row is a mock
'''

# ---------------------------------------------------------------------------- #

def main():

    N_mocks = 5000
    fid = 233

    # Load list of pointings
    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    # Load bins information -- this is made in a separate place
    bins_file = rbins_dir + 'rbins.ascii.dat'
    if not os.path.isfile(bins_file):
        sys.stderr.write('Error: ' + bins_file + ' does not exist.\n')

    bin_centers = np.genfromtxt(bins_file, skip_header=1, usecols=[2], unpack=True)
    N_bins      = len(bin_centers)

    # Round bin centers to three decimal places
    bin_centers = np.round(bin_centers, 3)

    # Make array of column names for pandas Dataframe
    col_names = []

    for i in range(N_bins):
        name = str(bin_centers[i])
        col_names.append(name)

    # Recast as array
    col_names = np.asarray(col_names)

    param_list = [183, 193, 203, 213, 223, 233, 243, 253, 263, 273, 283]

    for z in param_list:

        sys.stderr.write('z0_thin is 0.' + str(z) + '\n')

        mock_dir = '../5000_mocks_' + str(z) + '/errors_pairs/data/'

        if z == fid:
            mock_dir = '../../10000_mocks/errors_pairs/data/'

        # loop over each l.o.s.

        for p in todo_list:

            x = int(p.ID)
            if x%10 == 0:
                sys.stderr.write('Calculating stats for pointing {}\n'.format(p.ID))

            # Empty arrays where each row is counts for 1 mock in current l.o.s.
            DD_all = np.zeros((N_mocks, N_bins))

            # loop over all mocks
            for i in range(N_mocks):

                # Load counts for a single mock
                corr_file = ( mock_dir + 'mock_' + str(i+1) + '/mock_pairs_'
                            + p.ID + '.dat' )
                DD_all[i] = np.genfromtxt( corr_file, dtype=float, unpack=True,
                            usecols=[5] )

            # Output data
            output_filename = ( out_dir + 'z0thin_' + str(z) + '_normed_counts_all_'
                                + p.ID + '.dat')
            np.savetxt(output_filename, DD_all, fmt='%.6e')

            # Reload data as a pandas df because I'm stupid
            DF = pd.read_csv(output_filename, sep='\s+', names=col_names)

            corr = DF.corr()
            output_filename = out_dir + 'z0thin_' + str(z) + '_corr_mat_' + p.ID + '.dat'
            np.savetxt(output_filename, corr.values, fmt='%.6e')

if __name__ == '__main__':
    main()