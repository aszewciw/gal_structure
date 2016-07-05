from config import *

# ---------------------------------------------------------------------------- #

'''
For each l.o.s., calculate the density in different subvolumes of the pointing.
Then normalize each density by the average density in the whole pointing.
'''
# ---------------------------------------------------------------------------- #

def main():

    # Read in number of mocks
    elements_needed = int(2)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args   == elements_needed)
    N_mocks         = int(args_array[1])

    # load the todo pointing list
    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    # Mock numbering starts at 1 because I'm a jackass
    mock_nums = np.arange(N_mocks) + 1

    # load the bins list
    bins_file = data_dir + 'rbins.dat'
    rlower, rupper, volume = np.genfromtxt(bins_file, skip_header=1, unpack=True)
    Nbins = len(rlower)

    # get volume of whole pointing
    volume_los = np.sum(volume)

    # Loop over l.o.s.
    for p in todo_list:

        # Array of normalized density values for this pointing
        density_norm = np.zeros((N_mocks, Nbins))

        # a progress indicator
        sys.stderr.write('On pointing #{} of {} ..\n'
                         .format(todo_list.index(p), len(todo_list)))

        # Loop over different mocks
        for i in mock_nums:

            # Establish mock directory
            current_dir = mock_dir + 'mock_' + str(i) + '/'

            # Get xyz data
            mock_file = current_dir + 'mock_' + p.ID + '.xyz.dat'
            if not os.path.isfile(mock_file):
                sys.stderr.write('Error: ' + mock_file + ' does not exist.\n')
                continue

            x,y,z    = np.genfromtxt(mock_file, skip_header=1, unpack=True)
            distance = np.sqrt(x**2 + y**2 + z**2)

            # Total points in pointing
            N_points = len(x)

            # Average density of whole l.o.s.
            density_los = N_points / volume_los

            # Initialize counts in each sub-volume
            counts = np.zeros(Nbins)

            for j in range(Nbins):

                # Limits of current bin
                r1 = rlower[j]
                r2 = rupper[j]

                # Number of points in current sub-volume
                counts[j] = len( np.where((distance>r1)&(distance<=r2))[0] )

            # raw average density in each subvolume
            density_real = counts / volume

            # Normalize density and add to array
            # "i" is the mock number (1-1000); corresponding index is i-1
            density_norm[i-1] = density_real / density_los

        # Output file with all density values
        out_filename = data_dir + 'density_norm_' + p.ID + '.dat'
        np.savetxt(out_filename, density_norm)

        # Get averages and standard deviation
        averages = np.mean(density_norm, 0)
        stdev    = np.std(density_norm, 0)

        # Output file of average and std
        out_data     = np.column_stack((averages,stdev))
        out_filename = data_dir + 'ave_std_' + p.ID + '.dat'
        np.savetxt(out_filename, out_data)


if __name__ == '__main__':
    main()