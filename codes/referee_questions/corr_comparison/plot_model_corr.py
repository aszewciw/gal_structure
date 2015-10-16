import numpy as np
from config import *
import matplotlib.pyplot as plt
import matplotlib

'''
Read files of correlation data and plot them, including errors in mean
'''

def main():

    count = 0

    # Load todo list of pointings
    input_filename = data_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))

    with open(input_filename, 'rb') as input_file:
        todo_list = pickle.load(input_file)

    fig = plt.figure(figsize = (8, 7))
    ax1  = fig.add_subplot(1,1,1, axisbg = 'white')
    # ax2  = fig.add_subplot(2,1,2, axisbg = 'white', sharex=ax1)
    # ax2.set_xlabel('r (kpc)')
    ax1.set_ylabel(r'$\xi$(r)')
    ax1.set_xlabel('r (kpc)')
    # ax2.set_ylabel(r'$\xi_{PH}(r) - \xi_{LS}(r)$')



    # ax.set_xlabel('r (kpc)')
    # ax.set_ylabel(r'$\displaystyle\frac{DD}{MM}$(r) - 1')
    # ax.set_ylabel('Correlation(r)')
    ax1.set_title('Correlation for Milky Way Model')
    ax1.set_xscale('log')
    # ax2.set_xscale('log')

    plt.setp(ax1.get_xticklabels(), visible=False)
    # ax2.set_xticklabels(['0.01', '0.1', '1'])
    ax1.set_xticklabels(['0.01', '0.1', '1'])

    # ax2.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

    ax1.grid(True, color='k', linestyle = '--')
    # ax2.grid(True, color='k', linestyle = '--')

    # ax.set_zorder(1)
    # ax.set_axisbelow(True)


    for p in todo_list:

        # NE_file = data_dir + 'correlation_' + p.ID + '.dat'
        LS_file = MW_dir + 'MWcorr_' + p.ID + '.dat'

        # if (not os.path.isfile(NE_file)) or (not os.path.isfile(LS_file)):
        #     sys.stderr.write('Error: One file does not exist.\n')
        #     continue

        # bins, NE_corr = np.genfromtxt(NE_file, unpack=True, usecols=[0, 1])
        bins, LS_corr, DD, MM = np.genfromtxt(LS_file, unpack=True, usecols=[0, 1, 3, 5])
        NE_corr = np.zeros(len(LS_corr))
        for i in range(len(MM)):
            if MM[i] == 0:
                continue
            NE_corr[i] = DD[i] / MM[i] - 1

        Diff = NE_corr - LS_corr

        count += 1

        ax1.plot(bins, NE_corr, '0.6', zorder = -42)
        ax1.plot(bins, LS_corr, '0.9', zorder = -42)
        # ax2.plot(bins, Diff, '0.6', zorder = -42)
        # plt.axis([0.005, 2, -1, 1.5])
        ax1.set_xlim(0.005, 2)
        ax1.set_ylim(-1, 1.5)
        # ax2.set_ylim(-1, 1.5)

    sys.stderr.write('Total number of plots is {}\n'.format(count))

    # Load and plot files containing statistical data
    Diff_stats          = MW_dir + 'Mod_Diff_stats.dat'
    LS_stats            = MW_dir + 'Mod_LS_stats.dat'
    NE_stats            = MW_dir + 'Mod_NE_stats.dat'
    Diff_mean, Diff_err = np.genfromtxt(Diff_stats, unpack = True, usecols = [0, 2])
    LS_mean, LS_err     = np.genfromtxt(LS_stats, unpack = True, usecols = [0, 2])
    NE_mean, NE_err     = np.genfromtxt(NE_stats, unpack = True, usecols = [0, 2])

    # ax2.errorbar(bins, Diff_mean, Diff_err, fmt = 'go', ecolor = 'g', elinewidth = 1.5, capthick = 1.5, capsize = 7)
    ax1.errorbar(bins, LS_mean, LS_err, fmt = 'bo', ecolor = 'b', elinewidth = 1.5, capthick = 1.5, capsize = 7)
    ax1.errorbar(bins, NE_mean, NE_err, fmt = 'ro', ecolor = 'r', elinewidth = 1.5, capthick = 1.5, capsize = 7)

    plt.subplots_adjust(hspace=0.05)
    plt.show()

if __name__ == '__main__':
    main()
