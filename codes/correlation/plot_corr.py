import numpy as np
from config import *
import matplotlib.pyplot as plt

'''
Read files of correlation data and plot them, including errors
'''

def main():

    count = 0

    # Load todo list of pointings
    input_filename = data_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))

    with open(input_filename, 'rb') as input_file:
        todo_list = pickle.load(input_file)


    for p in todo_list:

        # filename = data_dir + 'correlation_' + p.ID + '.dat'
        filename = MW_dir + 'correlation_' + p.ID + '.dat'

        if not os.path.isfile(filename):
            sys.stderr.write('Error: ' + filename + ' does not exist.\n')
            continue

        bins, corr = np.genfromtxt(filename, unpack=True, usecols=[0, 1])

        count += 1

        plt.semilogx(bins, corr, '0.75', zorder = -42)
        plt.grid(True)
        plt.xlabel('r (kpc)')
        plt.ylabel('DD/MM - 1')
        plt.title('Two-point Correlation of SEGUE G-Dwarfs')
        plt.axis([0.005, 2, -1, 1.5])

    sys.stderr.write('Total number of plots is {}\n'.format(count))

    # Adding error bars
    stat_file = MW_dir + 'stat_data.dat'
    mean, error = np.genfromtxt(stat_file, unpack = True, usecols = [0, 2])
    plt.errorbar(bins, mean, error, fmt = 'ro', ecolor = 'r', elinewidth = 2, capthick = 2)
    plt.show()

if __name__ == '__main__':
    main()
