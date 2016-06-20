from config import *

def main():

    # Get which uniform type we want to use
    elements_needed = int(2)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args   == elements_needed)
    uni_type        = args_array[1]

    # load the todo pointing list
    input_filename = data_dir + 'corr_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    # calculate correlation function for each plate
    for p in corr_list:

        # random_file = data_dir + 'random_' + p.ID + '.xyzw.dat'
        random_file = data_dir + 'uniform_' + uni_type + '_' + p.ID + '.xyz.dat'

        star_file = data_dir + 'mock_full_' + p.ID + '.xyz.dat'

        if not os.path.isfile(random_file) or not os.path.isfile(star_file):
            sys.stderr.write('Error: ' + random_file
                             + ' or ' + star_file + ' does not exist.\n')
            continue

        output_file = data_dir + 'corr_full_' + uni_type + '_' + p.ID + '.dat'

        # parameters rmin, rmax, nbins
        param = '0.005 2.0, 12'

        cmd = ( './correlation ' + star_file + ' ' + random_file + ' '
            + param + ' > ' + output_file )

        os.system(cmd)


if __name__ == '__main__':
    main()

