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

    Nmock_list = [50, 100, 500, 1000, 5000, 10000]
    color_list = ['red', 'green', 'cyan', 'blue', 'black', 'magenta']

    np.random.seed()

    for ID in ID_list:

        if ID != '0':
            continue

        counts_file = mocks_dir + 'normed_counts_all_' + ID + '.dat'

        dd = np.genfromtxt(counts_file)

        plt.clf()
        plt.figure(1)

        for i in range(len(Nmock_list)):

            color=color_list[i]

            N = Nmock_list[i]

            np.random.shuffle(dd)

            dd_new = dd[:N]

            dd_mean = np.mean(dd_new, axis=0)
            dd_std  = np.std(dd_new, axis=0)
            print(dd_mean)

            plt.semilogx(bin_cent, dd_std, color=color, label='N='+str(N))

        plt.legend(loc='upper left')
        figname='std_' + ID + '.png'
        plt.savefig(figname)








if __name__ == '__main__':
    main()