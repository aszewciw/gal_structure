import pickle, sys, os
import numpy as np
import matplotlib.pyplot as plt
import math

rawdata_dir = '../../data/'
data_dir    = './data/'
counts_dir  = data_dir + 'counts/'

def main():

    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    mock_num = np.arange(1000) + 1

    # for p in todo_list:

    #     file = counts_dir + 'counts_' + p.ID + '.dat'

    ID = 100
    ID = str(ID)

    counts_file = counts_dir + 'counts_' + ID + '.dat'

    counts = np.genfromtxt(counts_file)

    bin_width = 2
    bin_min   = bin_width * math.floor(min(counts) / bin_width)
    bin_max   = bin_width * math.floor(max(counts) / bin_width)
    bins      = np.arange(bin_min, bin_max, bin_width)

    plt.clf()
    plt.figure(1)
    plt.hist(counts, bins)
    plt.xlabel('Number of Stars')
    plt.ylabel('Number of Mocks')
    plt.title('Line of Sight ' + ID)
    plt.savefig('los_' + ID + '.png')
    # plt.show()


if __name__ == '__main__':
    main()