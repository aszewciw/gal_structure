#!/usr/bin/env python

import sys, math, pickle, random
import config
import numpy as np

#------------------------------------------------------------------------------
def main():

    # load pointing list
    input_filename = config.todo_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file = open(input_filename, 'rb')
    todo_list = pickle.load(input_file)
    input_file.close()

    sys.stderr.write('Prepare mock files for correlation function calculation..\n')

    for p in todo_list:

        # star_filename = config.rawdata_dir + 'star_' + p.ID + '.dat'
        # star_file = open(star_filename, 'rb')
        # star_list = pickle.load(star_file)
        # star_file.close()

        # # random shuffle
        # random.shuffle(star_list)

        # # first output a full shuffled data set
        # output_filename = config.data_dir + 'star_' + p.ID + '_jk_all.dat'
        # output_file = open(output_filename, 'w')
        # # first output the total number of points
        # output_file.write('{}\n'.format(len(star_list)))
        # for s in star_list:
        #     output_file.write('{}\t{}\t{}\t{}\n'
        #                       .format(s.cartesian_x, s.cartesian_y, s.cartesian_z, s.weight))
        # output_file.close()

        mock_filename = config.mock_dir + 'mock_' + p.ID + '.xyz.dat'
        xyz = np.genfromtxt(mock_filename, skip_header=1)

        # random shuffle
        # random.shuffle(xyz)

        # first output a full shuffled data set
        output_filename = config.jk_dir + 'star_' + p.ID + '_jk_all.dat'
        output_file = open(output_filename, 'w')
        # first output the total number of points
        output_file.write('{}\n'.format(len(xyz)))
        # Output positions and weight of 1.0
        for i in range(len(xyz)):
            output_file.write('{}\t{}\t{}\t{}\n'
                              .format(xyz[i,0], xyz[i,1], xyz[i,2], 1.0))
        output_file.close()


        # make jackknife samples
        N_jackknife = config.N_jackknife # number of jackknife samples

        N = int(len(xyz) / N_jackknife)

        for i in range(N_jackknife):

            temp = xyz[:(N*i)]
            temp = np.append(temp, xyz[(N*i + N)])
            # output_list = star_list[:(N * i)] + star_list[(N * i + N):]

            output_filename = config.jk_dir + 'star_' + p.ID + '_jk_' + str(i) + '.dat'
            output_file = open(output_filename, 'w')
            # first output the total number of points
            output_file.write('{}\n'.format(len(temp)))
            # for s in output_list:
            #     output_file.write('{}\t{}\t{}\t{}\n'
            #                       .format(s.cartesian_x, s.cartesian_y, s.cartesian_z, s.weight))
            for j in range(len(temp)):
                output_file.write('{}\t{}\t{}\t{}\n'
                                  .format(temp[j,0], temp[j,1], temp[j,2], 1.0))

            output_file.close()

    sys.stderr.write('Jackknife sample output to {} . \n\n'.format(config.jk_dir))


if __name__ == '__main__' :
    main()





