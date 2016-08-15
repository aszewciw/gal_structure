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

        # Uniform points were randomly shuffled upon creation
        uni_filename = uniform_dir + 'uniform_' + p.ID + '.xyz.dat'
        xyz = np.genfromtxt( uni_filename, skip_header=1 )
        w = np.ones(len(xyz))
        xyzw = np.column_stack((xyz,w))

        # Output file with xyzw for all uniform points
        out_file = data_dir + 'uniform_' + p.ID + '.xyzw.dat'
        np.savetxt(out_file, xyzw, fmt='%1.6f')
        line_prepender(out_file, str(len(xyz)))

        # jackknife samples
        N_uni = len( xyzw )
        remain = N_uni % N_jackknife

        for i in range( N_jackknife ):

            # Make samples different sizes
            # Establish a slice to be deleted from array
            # slice_length = int( N_uni / N_jackknife )
            # lower_ind    = i * slice_length
            # if i < remain:
            #     lower_ind    += i
            #     slice_length += 1
            # else:
            #     lower_ind += remain
            # upper_ind = lower_ind + slice_length

            # Make every sub-sample the same size
            slice_length = int(N_uni / N_jackknife)
            lower_ind = i * slice_length
            upper_ind = lower_ind + slice_length
            remove_me = np.arange(lower_ind, upper_ind, 1)

            # Remove slice
            xyzw_temp = np.delete(xyzw, remove_me, 0)
            N_temp = len(xyzw_temp)

            # Output jackknife'd file
            out_file = data_dir + 'uniform_' + p.ID + '_jk_' + str(i) + '.dat'
            np.savetxt(out_file, xyzw_temp, fmt='%1.6f')

            # Add number of elements as first line in file
            line_prepender(out_file, str(N_temp))


    sys.stderr.write('Jackknife sample output to {} . \n\n'.format(data_dir))


if __name__ == '__main__' :
    main()
