'''
Contains histograms of the density distributions, produced from 1000 mocks.

Overplotted above the histogram is a Gaussian curve taken from the mean and
standard deviation.
'''

from config import *
import matplotlib.pyplot as plt

def main():

    # Number of mocks
    N_mocks = 1000

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
        if p.ID != '27':
            continue

        sys.stderr.write('Making histogram for pointing {}\n'.format(p.ID))

        # Empty arrays where each row is counts for 1 mock in current l.o.s.
        density_raw_all = np.zeros((N_mocks, N_bins))
        density_all     = np.zeros((N_mocks, N_bins))

        density_file = data_dir + 'density_norm_' + p.ID + '.dat'
        density_norm = np.genfromtxt(density_file)

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
            hist_bins = np.linspace(hist_min, hist_max, num=50)

            plt.clf()
            plt.figure(1)
            plt.hist(density, hist_bins, normed=1, color='blue')

            figure_name = ( plots_dir + 'histogram_' + p.ID + 'bin_' + str(i)
                            + '.png' )
            plt.savefig(figure_name)


if __name__ == '__main__':
    main()