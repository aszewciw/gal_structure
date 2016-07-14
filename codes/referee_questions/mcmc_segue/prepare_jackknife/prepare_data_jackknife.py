from config import *

#------------------------------------------------------------------------------#
'''
Jackknife data x,y,z data into N_jackknife samples. See config for number.
'''
#------------------------------------------------------------------------------#

def main():

    # load pointing list
    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    sys.stderr.write('Prepare data files for correlation function calculation...\n')

    for p in todo_list:

        # Load data file containing cartesian positions
        # datas were randomly shuffled upon creation -- no need to reshuffle
        data_filename = segue_dir + 'star_' + p.ID + '.xyz.dat'
        xyz = np.genfromtxt( data_filename, skip_header=1 )

        # jackknife samples
        N_data = len( xyz )
        # remain used to slice samples as evenly as possible
        remain = N_data % N_jackknife

        for i in range( N_jackknife ):

            # Establish a slice to be deleted from array
            # First get minimum size of slice and minimum lower index
            slice_length = int( N_data / N_jackknife )
            lower_ind    = i * slice_length

            # Correct length and lower index for uneven samples
            if i < remain:
                lower_ind    += i
                slice_length += 1
            else:
                lower_ind += remain

            # Get (excluded) upper index of slice
            upper_ind = lower_ind + slice_length

            # Get indices slice to be removed
            remove_me = np.arange(lower_ind, upper_ind, 1)

            # Remove slice
            xyz_temp = np.delete(xyz, remove_me, 0)
            N_temp   = len(xyz_temp)

            # Output jackknife'd file
            out_file = data_dir + 'star_' + p.ID + '_jk_' + str(i) + '.dat'
            np.savetxt(out_file, xyz_temp, fmt='%1.6f')

            # Add number of elements as first line in file
            N_temp   = len(xyz_temp)
            line_prepender(out_file, str(N_temp))


    sys.stderr.write('Jackknife sample output to {} . \n\n'.format(data_dir))


if __name__ == '__main__' :
    main()
