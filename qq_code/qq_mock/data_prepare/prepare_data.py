#!/usr/bin/env python

# import sys, math, pickle
# import config
from config import *

#------------------------------------------------------------------------------
def main():

    # load pointing list
    input_filename = data_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file = open(input_filename, 'rb')
    todo_list = pickle.load(input_file)
    input_file.close()

    sys.stderr.write('Prepare data files for correlation function calculation..\n')

    for p in todo_list:

        star_filename = mock_dir + 'mock_' + p.ID + '.xyz.dat'
        x,y,z = np.genfromtxt(star_filename, unpack=True, skip_header=1)

        N_stars = len(x)
        # star_filename = config.rawdata_dir + 'star_' + p.ID + '.dat'
        # star_file = open(star_filename, 'rb')
        # star_list = pickle.load(star_file)
        # star_file.close()

        # Convert to various coordinate systems
        # Initialize arrays
        ra_rad = np.zeros(N_stars)
        dec_rad = np.zeros(N_stars)
        distance = np.zeros(N_stars)
        l_rad = np.zeros(N_stars)
        b_rad = np.zeros(N_stars)
        gal_Z = np.zeros(N_stars)
        gal_R = np.zeros(N_stars)
        weight = np.ones(N_stars)

        for i in range(N_stars):
            ra_rad[i], dec_rad[i], distance[i] = cart2eq(x[i], y[i], z[i])
            l_rad[i], b_rad[i] = eq2gal(ra_rad[i], dec_rad[i])
            gal_Z[i], gal_R[i] = gal2ZR(l_rad[i], b_rad[i], distance[i])

        # output ascii file for correlation function calculation
        output_filename = data_dir + 'star_' + p.ID + '.ascii.dat'
        output_file = open(output_filename, 'w')
        # first output the total number of points
        output_file.write('{}\n'.format(N_stars))
        for i in range(N_stars):
            output_file.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'
                              .format(ra_rad[i], dec_rad[i], distance[i],
                                      l_rad[i], b_rad[i],
                                      gal_Z[i], gal_R[i],
                                      x[i], y[i], z[i],
                                      weight[i]))
        output_file.close()


if __name__ == '__main__' :
    main()





