import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

mocks_dir = '../10000_mocks/errors_pairs/data/'
todo_dir  = '../data/'
rbins_dir = '../mcmc_mock/data/rbins/'

def main():

    ID_file = todo_dir + 'pointing_ID.dat'
    ID_list = np.genfromtxt(ID_file, skip_header=1, dtype='str')

    bins_file = rbins_dir + 'rbins.ascii.dat'
    bin_cent = np.genfromtxt(bins_file, skip_header=1, unpack=True, usecols=[2])
    bin_cent = np.round(bin_cent, 3)

    Nmock_list = [50, 100, 500, 1000, 5000]
    color_list = ['red', 'green', 'cyan', 'blue', 'black']

    np.random.seed()

    for ID in ID_list:

        if ID != '0':
            continue

        counts_file = mocks_dir + 'normed_counts_all_' + ID + '.dat'

        dd = np.genfromtxt(counts_file)

        plt.clf()
        plt.figure(1)

        dd_mean_true = np.mean(dd, axis=0)
        dd_std_true = np.std(dd, axis=0)

        for i in range(len(Nmock_list)):

            color=color_list[i]

            N = Nmock_list[i]

            np.random.shuffle(dd)

            dd_new = dd[:N]

            dd_mean = np.mean(dd_new, axis=0)
            dd_std  = np.std(dd_new, axis=0)

            dd_std_frac = (dd_std - dd_std_true) / dd_std_true

            plt.semilogx(bin_cent, dd_std_frac, color=color, label='N='+str(N))

        plt.legend(loc='upper left', fontsize=10)
        plt.axis([min(bin_cent), max(bin_cent), -0.2, 0.2])
        # plt.axis([min(bin_cent), max(bin_cent), 0, 0.025])
        figname='std_' + ID + '.png'
        plt.xlabel('Bin Center (kpc)', fontsize=14)
        plt.ylabel(r'$\frac{\sigma_{N}-\sigma_{10000}}{\sigma_{10000}}$', fontsize=18)
        plt.savefig(figname)








if __name__ == '__main__':
    main()