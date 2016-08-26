#!/usr/bin/env python

import sys, math, pickle, random
import config

#------------------------------------------------------------------------------
def main():

    # load pointing list
    input_filename = config.data_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file = open(input_filename, 'rb')
    todo_list = pickle.load(input_file)
    input_file.close()

    sys.stderr.write('Prepare data files for correlation function calculation..\n')

    for p in todo_list:

        uniform_filename = config.data_dir + 'uniform_' + p.ID + '.dat'
        uniform_file = open(uniform_filename, 'rb')
        uniform_list = pickle.load(uniform_file)
        uniform_file.close()

        # random shuffle
        random.shuffle(uniform_list)

        # first output a full shuffled data set
        output_filename = config.data_dir + 'uniform_' + p.ID + '_jk_all.dat'
        output_file = open(output_filename, 'w')
        # first output the total number of points
        output_file.write('{}\n'.format(len(uniform_list)))
        for s in uniform_list:
            output_file.write('{}\t{}\t{}\t{}\n'
                              .format(s.cartesian_x, s.cartesian_y, s.cartesian_z, s.weight))
        output_file.close()

        # number of jackknife samples
        N_jackknife = config.N_jackknife

        N = int(len(uniform_list) / N_jackknife)

        for i in range(N_jackknife):
            output_list = uniform_list[:(N * i)] + uniform_list[(N * i + N):]

            output_filename = config.data_dir + 'uniform_' + p.ID + '_jk_' + str(i) + '.dat'
            output_file = open(output_filename, 'w')
            # first output the total number of points
            output_file.write('{}\n'.format(len(output_list)))
            for s in output_list:
                output_file.write('{}\t{}\t{}\t{}\n'
                                  .format(s.cartesian_x, s.cartesian_y, s.cartesian_z, s.weight))

            output_file.close()

    sys.stderr.write('Jackknife sample output to {} . \n\n'.format(config.data_dir))


if __name__ == '__main__' :
    main()





