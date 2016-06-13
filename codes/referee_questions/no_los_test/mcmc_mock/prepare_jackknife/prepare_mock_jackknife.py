from config import *

#------------------------------------------------------------------------------
def main():

    sys.stderr.write('Prepare mock files for correlation function calculation...\n')

    # Get xyz data of mock
    mock_filename = mock_dir + 'mock.xyz.dat'
    xyz = np.genfromtxt( mock_filename, skip_header=1 )
    N_mock = len(xyz)

    # Shuffle contents for jackknife
    np.random.seed()
    np.random.shuffle(xyz)

    # Find how many samples are of a longer length
    remain = N_mock % N_jackknife

    # Make jackknife samples
    for i in range( N_jackknife ):

        # Establish a sequential slice to be deleted from array
        # First get minimum size of slice and minimum lower index
        slice_length = int( N_mock / N_jackknife )
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
        out_file = data_dir + 'mock_jk_' + str(i) + '.dat'
        np.savetxt(out_file, xyz_temp, fmt='%1.6f')

        # Add number of elements as first line in file
        N_temp   = len(xyz_temp)
        line_prepender(out_file, str(N_temp))

    sys.stderr.write('Jackknife samples output to {} . \n'.format(data_dir))


if __name__ == '__main__' :
    main()
