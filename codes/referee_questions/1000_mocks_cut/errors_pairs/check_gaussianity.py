from config import *
import matplotlib.pyplot as plt
import pylab
from scipy.stats import norm

# ---------------------------------------------------------------------------- #
'''
Contains histograms of the pair count distributions, produced from 1000 mocks.

Overplotted above the histogram is a Gaussian curve taken from the mean and
standard deviation.
'''
# ---------------------------------------------------------------------------- #

def main():

    # Number of mocks
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

        # loop over all mocks and add DD values to array
        for i in range(N_mocks):

            # Load counts for a single mock
            corr_file = ( data_dir + 'mock_' + str(i+1) + '/mock_pairs_'
                + p.ID + '.dat' )
            DD_raw_all[i], DD_all[i] = np.genfromtxt( corr_file, unpack=True,
                usecols=[4, 5] )

        # Load mean and standard deviation
        stats_file = stats_dir + 'stats_' + p.ID + '.dat'
        mu_list, sigma_list = np.genfromtxt(stats_file, unpack=True,
                                usecols=[0,2])

        # Plot histogram for each bin
        for i in range(N_bins):

            # get current array for hist
            DD = DD_all[:, i]

            # Make histogram bins
            hist_min  = min(DD)
            hist_max  = max(DD)
            offset    = 0.001*hist_max
            hist_max  += offset # make sure max is in a bin
            N_hist    = 30
            hist_bins = np.linspace(hist_min, hist_max, num=50)

            # Get normalized counts, bin edges, bin centers
            counts, edges = np.histogram(DD, hist_bins, normed=True)
            binWidth      = edges[1] - edges[0]
            centers       = edges[:-1]+0.5*(edges[1:]-edges[:-1])

            # Plot bar graph with transparency
            # Multiply by binWidth because np.histogram divides by it by default
            plt.clf()
            plt.figure(1)
            plt.bar(centers, counts*binWidth, binWidth, color='blue', alpha=0.1)

            # Add a normal curve on top of the histogram
            mu    = mu_list[i]
            sigma = sigma_list[i]
            x     = np.linspace(centers[0], centers[-1], N_hist)
            plt.plot(x, norm.pdf(x, mu, sigma)*binWidth, color='r')

            # Save figure
            figure_name = ( plots_dir + 'histogram_' + p.ID + 'bin_' + str(i)
                            + '.png' )
            plt.savefig(figure_name)


if __name__ == '__main__':
    main()