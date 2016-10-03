import pickle, sys, os
import numpy as np
#------------------------------------------------------------------------------#
'''
Check whether any of the files in any of the mocks were not made.
Print out which ones and how many (if any).
'''
#------------------------------------------------------------------------------#
rawdata_dir = '../../data/'
data_dir    = './data/'
#------------------------------------------------------------------------------#

def main():

    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    mock_num = np.arange(1000) + 1
    count = 0
    for i in mock_num:

        mock_dir = data_dir + 'mock_' + str(i) + '/'

        for p in todo_list:

            filename = mock_dir + 'mock_' + p.ID + '.xyz.dat'

            if not os.path.isfile(filename):
                count+=1
                sys.stderr.write('Error: ' + filename + ' does not exist.\n')

    sys.stderr.write(str(count) + ' files do not exist.\n')

if __name__ == '__main__':
    main()