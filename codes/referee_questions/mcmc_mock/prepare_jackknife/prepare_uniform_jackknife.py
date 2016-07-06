from config import *

#------------------------------------------------------------------------------#
'''
Jackknife uniform x,y,z data into N_jackknife samples. See config for number.
'''
#------------------------------------------------------------------------------#
def main():

    # load pointing list
    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    sys.stderr.write('Prepare uniform files for correlation function calculation..\n')

    for p in todo_list:

        # Mocks were randomly shuffled upon creation
        uni_filename = uni_dir + 'uniform_' + p.ID + '.xyz.dat'
        xyz = np.genfromtxt( uni_filename, skip_header=1 )

        # jackknife samples
        N_uni = len( xyz )
        remain = N_uni % N_jackknife

        for i in range( N_jackknife ):

            # Establish a slice to be deleted from array
            slice_length = int( N_uni / N_jackknife )
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
            out_file = data_dir + 'uniform_' + p.ID + '_jk_' + str(i) + '.dat'
            np.savetxt(out_file, xyz_temp, fmt='%1.6f')

            # Add number of elements as first line in file
            line_prepender(out_file, str(N_temp))


    sys.stderr.write('Jackknife sample output to {} . \n\n'.format(data_dir))


if __name__ == '__main__' :
    main()
