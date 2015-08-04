#!/usr/bin/env python

from config import *

def main():

    # load the todo pointing list
    input_filename = data_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file = open(input_filename, 'r')
    todo_list = pickle.load(input_file)
    input_file.close()

    # calculate correlation function for each plate
    for p in todo_list:

        random_xyzw_filename = data_dir + 'random_' + p.ID + '.xyzw.dat'
        star_xyzw_filename = data_dir + 'star_' + p.ID + '.xyzw.dat'

        if not os.path.isfile(random_xyzw_filename) or not os.path.isfile(star_xyzw_filename):
            sys.stderr.write('Error: ' + random_file_name
                             + ' or ' + star_file_name + ' does not exist.\n')
            continue

        output_file = data_dir + 'correlation_' + p.ID + '.dat'

        # parameters rmin, rmax, nbins                                  The os.system command executes the string labeled cmd in a subshell
        param = '0.001 2.0 25'

        cmd = './correlation ' + star_xyzw_filename + ' ' + random_xyzw_filename + ' ' + param + ' > ' + output_file

        os.system(cmd)



if __name__ == '__main__' :
    main()


