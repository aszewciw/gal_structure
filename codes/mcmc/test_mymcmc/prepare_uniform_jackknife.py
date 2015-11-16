#!/usr/bin/env python

from config import *

#------------------------------------------------------------------------------
def main():

    # load pointing list
    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file = open(input_filename, 'rb')
    todo_list = pickle.load(input_file)
    input_file.close()

    sys.stderr.write('Prepare uniform files for correlation function calculation..\n')

    for p in todo_list:

        star_filename = uni_dir + 'uniform_' + p.ID + '.dat'
        star_file = open(star_filename, 'rb')
        star_list = pickle.load(star_file)
        star_file.close()

        # random shuffle
        random.shuffle(star_list)

        # first output a full shuffled data set
        output_filename = jk_dir + 'uniform_' + p.ID + '_jk_all.dat'
        output_file = open(output_filename, 'w')
        # first output the total number of points
        output_file.write('{}\n'.format(len(star_list)))
        for s in star_list:
            output_file.write('{}\t{}\t{}\t{}\n'
                              .format(s.cartesian_x, s.cartesian_y, s.cartesian_z, s.weight))
        output_file.close()

        N = len(star_list) / N_jackknife

        for i in range(N_jackknife):
            output_list = star_list[:int(N * i)] + star_list[int(N * i + N):]

            output_filename = jk_dir + 'uniform_' + p.ID + '_jk_' + str(i) + '.dat'
            output_file = open(output_filename, 'w')
            # first output the total number of points
            output_file.write('{}\n'.format(len(output_list)))
            for s in output_list:
                output_file.write('{}\t{}\t{}\t{}\n'
                                  .format(s.cartesian_x, s.cartesian_y, s.cartesian_z, s.weight))

            output_file.close()

    sys.stderr.write('Jackknife sample output to {} . \n\n'.format(jk_dir))


if __name__ == '__main__' :
    main()





