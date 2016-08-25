from config import *

def main():

    # load the todo pointing list
    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    # calculate correlation function for each plate
    for p in todo_list:


        # random_file = data_dir + 'random_' + p.ID + '.xyzw.dat'
        random_file = data_dir + 'MWM_' + p.ID + '.xyzw.dat'

        star_file = data_dir + 'mock_' + p.ID + '.xyzw.dat'

        if not os.path.isfile(random_file) or not os.path.isfile(star_file):
            sys.stderr.write('Error: ' + random_file
                             + ' or ' + star_file + ' does not exist.\n')
            continue

        output_file = data_dir + 'MWcorr_' + p.ID + '.dat'

        # parameters rmin, rmax, nbins
        # param = '0.001 2.0 25'
        param = '0.005 2.0, 12'

        cmd = ( './correlation ' + star_file + ' ' + random_file + ' '
            + param + ' > ' + output_file )

        os.system(cmd)


if __name__ == '__main__':
    main()

