'''
Calculate mock density and Poisson error in calculation.
'''
from config import *

def main():

    # Read in number of mocks
    elements_needed = int(2)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args   == elements_needed)
    N_mocks         = int(args_array[1])
    run_num         = int(args_array[2])

    # load the todo pointing list
    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    mock_nums = np.arange(N_mocks) + 1
    mock_nums += N_mocks * run_num

    # load the bins list
    bins_file = data_dir + 'rbins.dat'
    rlower, rupper, volume = np.genfromtxt(bins_file, skip_header=1,
        unpack=True)

    Nbins = len(rlower)

    # Loop over mocks
    for i in mock_nums:

        mock_dir = mock_dir + 'mock_' + str(i) + '/'
        out_dir  = data_dir + 'density_' + str(i) + '/'

        for p in todo_list:

            # a progress indicator
            if todo_list.index(p) % 10 == 0:
                sys.stderr.write('On pointing #{} of {} ..\n'
                                 .format(todo_list.index(p), len(todo_list)))

            mock_file = mock_dir + 'mock_' + p.ID + '.xyz.dat'
            x,y,z     = np.genfromtxt(mock_file, skip_header=1, unpack=True)
            distance  = np.sqrt(x**2 + y**2 + z**2)

            counts = np.zeros(Nbins)

            for i in range(Nbins):

                r1 = rlower[i]
                r2 = rupper[i]

                counts[i] = len( np.where((distance>r1)&(distance<=r2))[0] )

            density     = counts / volume

            output_file = density_dir + 'density_' + p.ID + '.dat'
            with open(output_file, 'w') as f:
                for j in range(Nbins):
                    f.write('{}\t{}\n'.format(counts[j], density[j])


if __name__ == '__main__':
    main()