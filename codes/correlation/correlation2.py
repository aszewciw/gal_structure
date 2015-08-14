#!/usr/bin/env python
'''Calculates the correlation function using KDTree mehod
from config import *
from scipy import spatial
import numpy as np


def count_pairs(xyz, weight):
    total = 0
    pair_count = np.zeros(len(bins) - 1)

    for i in range(len(xyz)):
        for j in range(i + 1, len(xyz)):
            dist_sq = np.sum((xyz[i] - xyz[j]) * (xyz[i] - xyz[j]))
            N_stars = weight[i] * weight[j]
            total += N_stars

            for k in range(len(pair_count)):
                if dist_sq > bins[k] and dist_sq <= bins[k + 1]:
                    pair_count[k] += N_stars
                    break

    pair_count /= total
    return pair_count


############################################

bin_min = 0.001
bin_max = 2
N_bins = 26
bins = np.linspace(math.log(bin_min), math.log(bin_max), N_bins)
bins = np.exp(bins)
bins = bins ** 2

def main():


    bin_min = 0.001
    bin_max = 2
    N_bins = 26
    bins = np.linspace(math.log(bin_min), math.log(bin_max), N_bins)
    bins = np.exp(bins)
    bins = bins ** 2
    rand_counts = np.genfromtxt('random_counts.txt')

    #load the list of pointings on which we'll run correlation
    input_filename = data_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))

    with open(input_filename, 'rb') as input_file:
        todo_list = pickle.load(input_file)

    for p in todo_list:

        star_xyzw_filename = data_dir + 'star_' + p.ID + '.xyzw.dat'

        if not os.path.isfile(star_xyzw_filename):
            sys.stderr.write('Error: ' + star_file_name + ' does not exist.\n')
            continue

        star_xyz = np.genfromtxt(star_xyzw_filename, usecols = [0, 1, 2])
        star_w = np.genfromtxt(star_xyzw_filename, usecols = [3])

        star_pairs = count_pairs(star_xyz, star_w)

        corr = star_pairs / rand_counts - 1

        np.savetxt(data_dir + 'correlation_' + p.ID +'.dat', corr)


if __name__ == '__main__':
    main()