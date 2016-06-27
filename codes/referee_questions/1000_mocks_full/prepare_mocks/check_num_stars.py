import pickle, sys, os
import numpy as np

rawdata_dir = '../../data/'
data_dir    = './data/'
counts_dir  = data_dir + 'counts/'

def main():

    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    mock_num = np.arange(1000) + 1
    counts = {}

    for p in todo_list:

        counts[p.ID] = np.zeros(1000)

    for i in mock_num:

        mock_dir = data_dir + 'mock_' + str(i) + '/'

        index_num = i - 1

        for p in todo_list:

            sys.stderr.write('On pointing number ' + p.ID + '\n')

            filename = mock_dir + 'mock_' + p.ID + '.xyz.dat'

            if not os.path.isfile(filename):
                sys.stderr.write('Error: ' + filename + ' does not exist.\n')
                continue

            with open(filename, 'r') as f:
                temp = f.readline().strip()

            counts[p.ID][index_num] = int(temp)

    for p in todo_list:

        out_file = counts_dir + 'counts_' + p.ID + '.dat'

        array = counts[p.ID]

        np.savetxt(out_file, array)


    sys.stderr.write(str(count) + ' files do not exist.\n')

if __name__ == '__main__':
    main()