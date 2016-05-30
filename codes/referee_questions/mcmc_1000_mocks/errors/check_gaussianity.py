'''
Produces histograms for all bins for whichever l.o.s.
I choose.
As of now, there is no intelligent place of storing these
files because I just wanted to check the Gaussianity of a
few.

It looks good.

'''



from config import *
import matplotlib.pyplot as plt

def main():

    N_mocks = 1000

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

        if p.ID != '27':
            continue

        sys.stderr.write('Making histogram for pointing {}\n'.format(p.ID))

        # Empty arrays where each row is counts for 1 mock in current l.o.s.
        DD_raw_all = np.zeros((N_mocks, N_bins))
        DD_all     = np.zeros((N_mocks, N_bins))

        # loop over all mocks
        for i in range(N_mocks):

            # Load counts for a single mock
            corr_file = ( mock_dir + 'mock_' + str(i+1) + '/mock_pairs_'
                + p.ID + '.dat' )
            DD_raw_all[i], DD_all[i] = np.genfromtxt( corr_file, unpack=True,
                usecols=[4, 5] )


        # Plot histogram for each bin
        for i in range(N_bins):

            # get current array for hist
            DD = DD_raw_all[:, i]

            # Make histogram bins
            hist_min  = min(DD)
            hist_max  = max(DD)
            offset    = 0.001*hist_max
            hist_max  += offset # make sure max is in a bin
            N_hist    = 30
            hist_bins = np.linspace(hist_min, hist_max, num=50)

            plt.clf()
            plt.figure(1)
            plt.hist(DD, hist_bins, color='blue')

            figure_name = 'histogram_bin_' + str(i) + '.png'
            plt.savefig(figure_name)


if __name__ == '__main__':
    main()