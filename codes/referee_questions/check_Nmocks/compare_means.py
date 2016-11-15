import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

mocks_dir = '../10000_mocks/errors_pairs/data/'
todo_dir  = '../data/'
rbins_dir = '../mcmc_mock/data/rbins/'

#------------------------------------------------------------------------------#
def GIF_MOVIE(files, output_gif, delay=60, repeat=True, removef=False):
    """
    Given a list if 'files', it creates a gif file, and deletes temp files.

    Parameters
    ----------
    files: array_like
            List of abs. paths to temporary figures

    output_gif: str
            Absolute path to output gif file.
    """
    loop = -1 if repeat else 0
    os.system('convert -delay %d -loop %d %s %s' %( delay,loop," ".join(files), \
        output_gif) )

    if removef:
        for fname in files: os.remove(fname)

#------------------------------------------------------------------------------#

def main():

    ID_file = todo_dir + 'pointing_ID.dat'
    ID_list = np.genfromtxt(ID_file, skip_header=1, dtype='str')

    bins_file = rbins_dir + 'rbins.ascii.dat'
    bin_cent = np.genfromtxt(bins_file, skip_header=1, unpack=True, usecols=[2])
    bin_cent = np.round(bin_cent, 3)

    Nmock_list = [50, 100, 500, 1000, 5000]
    color_list = ['red', 'yellow', 'green', 'blue', 'magenta']

    file_list = []

    np.random.seed()

    for ID in ID_list:

        counts_file = mocks_dir + 'normed_counts_all_' + ID + '.dat'

        dd = np.genfromtxt(counts_file)

        plt.clf()
        plt.figure(1)

        dd_mean_true = np.mean(dd, axis=0)

        for i in range(len(Nmock_list)):

            color=color_list[i]

            N = Nmock_list[i]

            np.random.shuffle(dd)

            dd_new = dd[:N]

            dd_mean = np.mean(dd_new, axis=0)

            dd_mean_frac = (dd_mean - dd_mean_true) / dd_mean_true

            plt.semilogx(bin_cent, dd_mean_frac, color=color, label='N='+str(N))

        plt.legend(loc='upper left', fontsize=10)
        plt.axis([min(bin_cent), max(bin_cent), -0.2, 0.2])
        figname='mean_' + ID + '.png'
        plt.xlabel('Bin Center (kpc)', fontsize=10)
        plt.ylabel(r'$\frac{\bar{DD_{N}}-\bar{DD_{10000}}}{\bar{DD_{10000}}}$', fontsize=18)
        plt.savefig(figname)

        file_list.append(figname, removef=True)

    gif_name = 'means.gif'








if __name__ == '__main__':
    main()