# from config import *

# #------------------------------------------------------------------------------#
# '''
# Jackknife uniform x,y,z data into N_jackknife samples. See config for number.
# '''
# #------------------------------------------------------------------------------#
# def main():

#     # load pointing list
#     input_filename = rawdata_dir + 'todo_list.dat'
#     sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
#     input_file     = open(input_filename, 'rb')
#     todo_list      = pickle.load(input_file)
#     input_file.close()

#     sys.stderr.write('Prepare uniform files for correlation function calculation..\n')

#     for p in todo_list:

#         # Mocks were randomly shuffled upon creation
#         uni_filename = uni_dir + 'uniform_' + p.ID + '.xyz.dat'
#         xyz = np.genfromtxt( uni_filename, skip_header=1 )

#         # jackknife samples
#         N_uni = len( xyz )
#         remain = N_uni % N_jackknife

#         for i in range( N_jackknife ):

#             # Make samples different sizes
#             # Establish a slice to be deleted from array
#             # slice_length = int( N_uni / N_jackknife )
#             # lower_ind    = i * slice_length
#             # if i < remain:
#             #     lower_ind    += i
#             #     slice_length += 1
#             # else:
#             #     lower_ind += remain
#             # upper_ind = lower_ind + slice_length

#             # Make every sub-sample the same size
#             slice_length = int(N_uni / N_jackknife)
#             lower_ind = i * slice_length
#             upper_ind = lower_ind + slice_length
#             remove_me = np.arange(lower_ind, upper_ind, 1)

#             # Remove slice
#             xyz_temp = np.delete(xyz, remove_me, 0)
#             N_temp = len(xyz_temp)

#             # Output jackknife'd file
#             out_file = data_dir + 'uniform_' + p.ID + '_jk_' + str(i) + '.dat'
#             np.savetxt(out_file, xyz_temp, fmt='%1.6f')

#             # Add number of elements as first line in file
#             line_prepender(out_file, str(N_temp))


#     sys.stderr.write('Jackknife sample output to {} . \n\n'.format(data_dir))


# if __name__ == '__main__' :
#     main()

#!/usr/bin/env python

import sys, math, pickle, random
import config

#------------------------------------------------------------------------------
def main():

    # load pointing list
    input_filename = config.rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file = open(input_filename, 'rb')
    todo_list = pickle.load(input_file)
    input_file.close()

    sys.stderr.write('Prepare data files for correlation function calculation..\n')

    for p in todo_list:

        uniform_filename = config.uni_dir + 'uniform_' + p.ID + '.dat'
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
