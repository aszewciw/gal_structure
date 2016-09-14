from config import *

#------------------------------------------------------------------------------#
'''
Jackknife mock x,y,z data into N_jackknife samples. See config for number.
'''
#------------------------------------------------------------------------------#

def main():

    # load pointing list
    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    sys.stderr.write('Prepare mock files for correlation function calculation...\n')

    for p in todo_list:

        # Load data file containing cartesian positions
        data_filename = mock_dir + 'mock_' + p.ID + '.xyz.dat'
        # xyz = np.genfromtxt( data_filename, skip_header=1 )
        x,y,z = np.genfromtxt(data_filename, unpack=True, skip_header=1)
        N_stars = len(x)
        weight = np.ones(N_stars)

        # np.random.shuffle(xyz)

        # jackknife samples
        # N_data = len( xyz )
        # remain used to slice samples as evenly as possible
        # remain = N_data % N_jackknife
        output_filename = data_dir + 'mock_' + p.ID + '_jk_all.dat'
        output_file = open(output_filename, 'w')
        # first output the total number of points
        output_file.write('{}\n'.format(N_stars))
        for i in range(N_stars):
            output_file.write('{}\t{}\t{}\t{}\n'
                              .format(x[i], y[i], z[i], weight[i]))
        output_file.close()

        N = int(N_stars / N_jackknife)

        for i in range( N_jackknife ):

            # # Make samples different sizes
            # # Establish a slice to be deleted from array
            # # slice_length = int( N_data / N_jackknife )
            # # lower_ind    = i * slice_length
            # # if i < remain:
            # #     lower_ind    += i
            # #     slice_length += 1
            # # else:
            # #     lower_ind += remain
            # # upper_ind = lower_ind + slice_length

            # # Make every sub-sample the same size
            # slice_length = int(N_data / N_jackknife)
            # lower_ind = i * slice_length
            # upper_ind = lower_ind + slice_length
            # remove_me = np.arange(lower_ind, upper_ind, 1)

            # # Remove slice
            # xyz_temp = np.delete(xyz, remove_me, 0)
            # N_temp   = len(xyz_temp)

            # # Output jackknife'd file
            # out_file = data_dir + 'mock_' + p.ID + '_jk_' + str(i) + '.dat'
            # np.savetxt(out_file, xyz_temp, fmt='%1.6f')

            # # Add number of elements as first line in file
            # N_temp   = len(xyz_temp)
            # line_prepender(out_file, str(N_temp))
            cartesian_x = x[:(N*i)]
            cartesian_x = np.append(cartesian_x, x[(N*i+N):], axis=0)
            cartesian_y = y[:(N*i)]
            cartesian_y = np.append(cartesian_y, y[(N*i+N):], axis=0)
            cartesian_z = z[:(N*i)]
            cartesian_z = np.append(cartesian_z, z[(N*i+N):], axis=0)
            w = weight[:(N*i)]
            w = np.append(w, weight[(N*i+N):], axis=0)

            N_stars_jk = len(cartesian_x)
            output_filename = data_dir + 'mock_' + p.ID + '_jk_' + str(i) + '.dat'
            output_file = open(output_filename, 'w')
            # first output the total number of points
            output_file.write('{}\n'.format(N_stars_jk))
            for j in range(N_stars_jk):
                output_file.write('{}\t{}\t{}\t{}\n'
                                  .format(cartesian_x[j], cartesian_y[j], cartesian_z[j], w[j]))

            output_file.close()


    sys.stderr.write('Jackknife sample output to {} . \n\n'.format(data_dir))


if __name__ == '__main__' :
    main()
