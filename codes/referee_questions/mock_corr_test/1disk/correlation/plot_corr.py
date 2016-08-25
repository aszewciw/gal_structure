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
    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))

    with open(input_filename, 'rb') as input_file:
        todo_list = pickle.load(input_file)

    plt.clf()

    fig = plt.figure(figsize = (10, 8))
    ax = fig.add_subplot(1,1,1, axisbg = 'white')
    ax.set_xlabel('r (kpc)')
    ax.set_ylabel(r'$\displaystyle\frac{DD}{MM}$(r) - 1')
    ax.set_title('Mock vs. weighted randoms of same params')
    ax.set_xscale('log')
    # ax.set_xticks([0.01, 0.1, 1])
    ax.set_xticklabels(['0.01', '0.1', '1'])
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

    ax.grid(True, color='k', linestyle = '--')
    # ax.set_zorder(1)
    # ax.set_axisbelow(True)


    for p in todo_list:

        # filename = data_dir + 'correlation_' + p.ID + '.dat'
        filename = data_dir + 'MWcorr_' + p.ID + '.dat'

        if not os.path.isfile(filename):
            sys.stderr.write('Error: ' + filename + ' does not exist.\n')
            continue

        bins, corr = np.genfromtxt(filename, unpack=True, usecols=[0, 1])

        count += 1

        # plt.semilogx(bins, corr, '0.75', zorder = -42)
        # ax.semilogx(bins, corr, '0.75', zorder = -42)
        ax.plot(bins, corr, '0.75', zorder = -42)
        # ax.set_zorder(10)
        # plt.grid(True)
        # plt.xlabel(r'\ r (kpc)')
        # plt.ylabel(r'$\displaystyle\frac{DD}{MM}$(r) - 1')

        # plt.title('Two-point Correlation of SEGUE G-Dwarfs')
        plt.axis([0.005, 2, -1, 1.5])

    sys.stderr.write('Total number of plots is {}\n'.format(count))

    # Adding error bars
    stat_file = data_dir + 'stat_data.dat'
    mean, error = np.genfromtxt(stat_file, unpack = True, usecols = [0, 2])
    # plt.errorbar(bins, mean, error, fmt = 'ro', ecolor = 'r', elinewidth = 1.5, capthick = 1.5)
    ax.errorbar(bins, mean, error, fmt = 'ro', ecolor = 'r', elinewidth = 1.5, capthick = 1.5, capsize = 7)
    # ax.set_zorder(20)

    fig_name = data_dir + '1disk_mock_vs_weights.png'
    plt.savefig(fig_name)
    plt.clf()

if __name__ == '__main__':
    main()
