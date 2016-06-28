'''
Loops over all SEGUE los and produces a file for each
mock containing the normalized dd counts.
'''

from config import *

def main():

    # Read in number of mocks
    elements_needed = int(2)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args   == elements_needed)
    N_mocks         = int(args_array[1])

    # Load list of pointings
    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    # Load bins information
    bins_file = bins_dir + 'rbins.ascii.dat'
    if not os.path.isfile(bins_file):
        sys.stderr.write('Error: ' + bins_file + ' does not exist.\n')

    # Loop over mocks
    for i in range(N_mocks):

        # First remove any existing files
        cmd = 'rm ' + data_dir + 'mock_' + str(i+1) + '/mock_pairs*'
        os.system(cmd)

        # Loop over l.o.s.
        for p in todo_list:

            # Notice extenstions for each mock directory
            in_file = ( mock_dir + 'mock_' + str(i+1) + '/mock_' + p.ID
                + '.xyz.dat' )

            if not os.path.isfile(in_file):
                sys.stderr.write('Error: ' + in_file + ' does not exist.\n')
                continue

            output_file = ( data_dir + 'mock_' + str(i+1) + '/mock_pairs_'
                + p.ID + '.dat' )

            cmd = ( './mock_pair_count ' + in_file + ' ' + bins_file
                + ' > ' + output_file )
            os.system(cmd)

if __name__ == '__main__':
    main()