from config import *

## ------------------------------------------------------------------------- ##

def line_prepender(filename, line):
    '''
    Appends a line to the beginning of a file.

    Arguments:
    1. filename : (str) name of file
    2. line : (str) line to be appended
    '''
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

#------------------------------------------------------------------------------
def main():

    # load pointing list
    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    sys.stderr.write('Prepare mock files for correlation function calculation..\n')

    for p in todo_list:

        # star_filename = config.rawdata_dir + 'star_' + p.ID + '.dat'
        # star_file = open(star_filename, 'r')
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

        # # make jackknife samples
        # N = N_mock / N_jackknife

        # for i in range(N_jackknife):
        #     output_list = star_list[:(N * i)] + star_list[(N * i + N):]

        #     output_filename = config.data_dir + 'star_' + p.ID + '_jk_' + str(i) + '.dat'
        #     output_file = open(output_filename, 'w')
        #     # first output the total number of points
        #     output_file.write('{}\n'.format(len(output_list)))
        #     for s in output_list:
        #         output_file.write('{}\t{}\t{}\t{}\n'
        #                           .format(s.cartesian_x, s.cartesian_y, s.cartesian_z, s.weight))

        #     output_file.close()

        # Mocks were randomly shuffled upon creation
        mock_filename = mock_dir + 'mock_' + p.ID + '.xyz.dat'
        xyz = np.genfromtxt( mock_filename, skip_header=1 )

        # jackknife samples
        N_mock = len( xyz )
        remain = N_mock % N_jackknife

        for i in range( N_jackknife ):

            # Establish a slice to be deleted from array
            slice_length = int( N_mock / N_jackknife )
            lower_ind    = i * slice_length
            if i < remain:
                lower_ind    += i
                slice_length += 1
            else:
                lower_ind += remain
            upper_ind = lower_ind + slice_length
            remove_me = np.arange(lower_ind, upper_ind, 1)

            # Remove slice
            xyz_temp = np.delete(xyz, remove_me, 0)
            N_temp = len(xyz_temp)

            # Output jackknife'd file
            out_file = data_dir + 'mock_' + p.ID + '_jk_' + str(i) + '.dat'
            np.savetxt(out_file, xyz_temp, fmt='%1.6f')

            # Add number of elements as first line in file
            line_prepender(out_file, str(N_temp))


    sys.stderr.write('Jackknife sample output to {} . \n\n'.format(data_dir))


if __name__ == '__main__' :
    main()





