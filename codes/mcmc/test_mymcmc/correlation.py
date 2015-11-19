#!/usr/bin/env python
'''
Loads each data and random(or model) file and runs correlation on them
using a c file.

'''

from config import *

def main():

    # load the todo pointing list
    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file = open(input_filename, 'rb')
    todo_list = pickle.load(input_file)
    input_file.close()

    # calculate correlation function for each plate
    for p in todo_list:

        random_xyzw_filename = uni_dir + 'weighted_' + p.ID + '.dat'

        star_xyzw_filename = data_dir + 'mock_' + p.ID + '.xyzw.dat'

        if not os.path.isfile(random_xyzw_filename) or not os.path.isfile(star_xyzw_filename):
            sys.stderr.write('Error: ' + random_xyzw_filename
                             + ' or ' + star_xyzw_filename + ' does not exist.\n')
            continue

        output_file = corr_dir + 'correlation_' + p.ID + '.dat'

        # parameters rmin, rmax, nbins
        param = '0.001 2.0 12'

        cmd = './correlation ' + star_xyzw_filename + ' ' + random_xyzw_filename + ' ' + param + ' > ' + output_file

        os.system(cmd)


if __name__ == '__main__' :
    main()


