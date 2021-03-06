from config import *
import matplotlib.pyplot as plt
import pylab
from scipy.stats import norm

# ---------------------------------------------------------------------------- #
'''
Contains histograms of the density distributions, produced from 1000 mocks.

Overplotted above the histogram is a Gaussian curve taken from the mean and
standard deviation.
'''
# ---------------------------------------------------------------------------- #

def main():

    # Number of mocks
    N_mocks = 10000

    # Load list of pointings
    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    # Load bins information -- this is made in a separate place
    bins_file = data_dir + 'rbins.dat'
    if not os.path.isfile(bins_file):
        sys.stderr.write('Error: ' + bins_file + ' does not exist.\n')

    # We really just want the number of bins
    with open(bins_file) as b:
        N_bins = int(b.readline())

    # loop over each l.o.s.
    for p in todo_list:

        # Select pointing to make plot of
        if p.ID != '28':
            continue

        sys.stderr.write('Making histogram for pointing {}\n'.format(p.ID))

        # Empty arrays where each row is counts for 1 mock in current l.o.s.
        density_raw_all = np.zeros((N_mocks, N_bins))
        density_all     = np.zeros((N_mocks, N_bins))

        # Load array of density values
        density_file = data_dir + 'density_norm_' + p.ID + '.dat'
        density_norm = np.genfromtxt(density_file)

        # Load mean and standard deviation
        stats_file = data_dir + 'ave_std_' + p.ID + '.dat'
        mu_list, sigma_list = np.genfromtxt(stats_file, unpack=True)

        # Plot histogram for each bin
        for i in range(N_bins):

            # get current array for hist
            density = density_norm[:, i]

            # Make histogram bins
            hist_min  = min(density)
            hist_max  = max(density)
            offset    = 0.001*hist_max
            hist_max  += offset # make sure max is in a bin
            N_hist    = 30
            hist_bins = np.linspace(hist_min, hist_max, num=N_hist)

            # Get normalized counts, bin edges, bin centers
            counts, edges = np.histogram(density, hist_bins, normed=True)
            binWidth      = edges[1] - edges[0]
            centers       = edges[:-1]+0.5*(edges[1:]-edges[:-1])

            # Plot bar graph with transparency
            # Multiply by binWidth because np.histogram divides by it by default
            plt.clf()
            plt.figure(1)
            plt.bar(centers, counts*binWidth, binWidth, color='blue', alpha=0.1)

            # Get Stats for this bin
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