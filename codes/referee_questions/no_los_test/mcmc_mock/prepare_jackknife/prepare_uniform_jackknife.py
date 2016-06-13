from config import *

#------------------------------------------------------------------------------
def main():

    sys.stderr.write('Prepare uniform files for correlation function calculation..\n')

    # Uniform points were randomly created - no shuffle needed
    uni_filename = uni_dir + 'random_xyz.dat'
    xyz = np.genfromtxt( uni_filename, skip_header=1 )
    N_uni = len( xyz )

    # Find how many samples are of a longer length
    remain = N_uni % N_jackknife

    # Make jackknife samples
    for i in range( N_jackknife ):

        # Establish a slice to be deleted from array
        slice_length = int( N_uni / N_jackknife )
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
        N_temp = len(xyz_temp)

        # Output jackknife'd file
        out_file = data_dir + 'uniform_jk_' + str(i) + '.dat'
        np.savetxt(out_file, xyz_temp, fmt='%1.6f')

        # Add number of elements as first line in file
        line_prepender(out_file, str(N_temp))


    sys.stderr.write('Jackknife sample output to {} . \n\n'.format(data_dir))


if __name__ == '__main__' :
    main()
