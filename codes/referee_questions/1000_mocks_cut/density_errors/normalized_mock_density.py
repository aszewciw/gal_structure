'''
For each l.o.s., calculate the density in different subvolumes of the pointing.
Then normalize each density by the average density in the whole pointing.
'''
from config import *

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

    mock_nums = np.arange(N_mocks) + 1

    # load the bins list
    bins_file = data_dir + 'rbins.dat'
    rlower, rupper, volume = np.genfromtxt(bins_file, skip_header=1,
        unpack=True)

    # get volume of whole pointing
    volume_los = np.sum(volume)

    Nbins = len(rlower)

    # Loop over l.o.s.
    for p in todo_list:

        # Array of normalized density values for this pointing
        density_norm = np.zeros((N_mocks, Nbins))

        # a progress indicator
        # if todo_list.index(p) % 10 == 0:
        sys.stderr.write('On pointing #{} of {} ..\n'
                         .format(todo_list.index(p), len(todo_list)))

        for i in mock_nums:

            current_dir = mock_dir + 'mock_' + str(i) + '/'

            mock_file = current_dir + 'mock_' + p.ID + '.xyz.dat'
            if not os.path.isfile(mock_file):
                sys.stderr.write('Error: ' + mock_file + ' does not exist.\n')
                continue

            x,y,z     = np.genfromtxt(mock_file, skip_header=1, unpack=True)
            distance  = np.sqrt(x**2 + y**2 + z**2)

            counts = np.zeros(Nbins)

            for j in range(Nbins):

                r1 = rlower[j]
                r2 = rupper[j]

                counts[j] = len( np.where((distance>r1)&(distance<=r2))[0] )

            # raw density in each subvolume
            density_real = counts / volume

            # average density in whole l.o.s.
            N_points = len(distance)
            density_los = N_points / volume_los

            # Normalize density and add to array
            density_norm[i-1] = density_real / density_los

        # Output file with all density values
        out_filename = data_dir + 'density_norm_' + p.ID + '.dat'
        np.savetxt(out_filename, density_norm)

        # Get averages and standard deviation
        averages = np.mean(density_norm, 0)

        stdev = np.std(density_norm, 0)

        out_data = np.column_stack((averages,stdev))

        out_filename = data_dir + 'ave_std_' + p.ID + '.dat'

        np.savetxt(out_filename, out_data)


if __name__ == '__main__':
    main()