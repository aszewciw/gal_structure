#!/usr/bin/env python

'''
This is incredibly dumb, but I need to do some manipulation to use his files...
'''

import sys, math, pickle, random
import config
import numpy as np

#------------------------------------------------------------------------------
def main():

    # load pointing list
    input_filename = config.data_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file = open(input_filename, 'rb')
    todo_list = pickle.load(input_file)
    input_file.close()

    sys.stderr.write('Prepare data files for correlation function calculation..\n')


    star_list = []

    for p in todo_list:

        star_filename = config.mock_dir + 'mock_' + p.ID + '.xyz.dat'
        x,y,z = np.genfromtxt(star_filename, unpack=True, skip_header=1)
        N_stars = len(x)
        weight = np.ones(N_stars)

        # for i in range(N_stars):
        #     s = Star()
        #     s.cartesian_x = x[i]
        #     s.cartesian_y = y[i]
        #     s.cartesian_z = z[i]
        #     s.weight = 1.0

        #     star_list.append(s)

        # # random shuffle
        # random.shuffle(star_list)

        # first output a full shuffled data set
        output_filename = config.data_dir + 'star_' + p.ID + '_jk_all.dat'
        output_file = open(output_filename, 'w')
        # first output the total number of points
        output_file.write('{}\n'.format(N_stars)
        for i in range(N_stars:
            output_file.write('{}\t{}\t{}\t{}\n'
                              .format(x[i], y[i], z[i], weight[i]))
        output_file.close()


        # make jackknife samples
        N_jackknife = config.N_jackknife # number of jackknife samples

        N = int(len(star_list) / N_jackknife)

        for i in range(N_jackknife):
            # output_list = star_list[:(N * i)] + star_list[(N * i + N):]
            cartesian_x = x[:(N*i)]
            np.append(cartesian_x, x[(N*i+N):])
            cartesian_y = y[:(N*i)]
            np.append(cartesian_y, y[(N*i+N):])
            cartesian_z = z[:(N*i)]
            np.append(cartesian_z, z[(N*i+N):])
            w = weight[:(N*i)]
            np.append(w, weight[(N*i+N):])

            N_stars_jk = len(cartesian_x)
            output_filename = config.data_dir + 'star_' + p.ID + '_jk_' + str(i) + '.dat'
            output_file = open(output_filename, 'w')
            # first output the total number of points
            output_file.write('{}\n'.format(N_stars_jk))
            for j in range(N_stars_jk):
                output_file.write('{}\t{}\t{}\t{}\n'
                                  .format(cartesian_x[j], cartesian_y[j], cartesian_z[j], w[j]))

            output_file.close()

    sys.stderr.write('Jackknife sample output to {} . \n\n'.format(config.data_dir))


if __name__ == '__main__' :
    main()





