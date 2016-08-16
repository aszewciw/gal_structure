from config import *

#------------------------------------------------------------------------------#
'''
Jackknife uniform x,y,z data into N_jackknife samples. See config for number.
'''
#------------------------------------------------------------------------------#
def main():

    # Tell which model to use. See rand_to_model.py for params
    elements_needed = int(2)
    args_array = np.array(sys.argv)
    N_args = len(args_array)
    assert(N_args == elements_needed)
    model = int(args_array[1])

    # load pointing list
    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    sys.stderr.write('Prepare uniform files for correlation function calculation..\n')

    for p in todo_list:

        # We already have an xyzw file

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
            out_file = ( data_dir + 'MWM_type' + str(model) + '_' + p.ID
                + '_jk_' + str(i) + '.dat' )
            np.savetxt(out_file, xyzw_temp, fmt='%1.6f')

            # Add number of elements as first line in file
            line_prepender(out_file, str(N_temp))


    sys.stderr.write('Jackknife sample output to {} . \n\n'.format(data_dir))


if __name__ == '__main__' :
    main()
