
from config import *
import numpy as np

'''
This calculates the mean, standard deviation, and error of the
correlation between data and MW model points. It reads in correlation
files and writes a single data file containing the statistical information.

'''

def main():

    # load the todo pointing list
    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    with open(input_filename, 'rb') as todo:
        todo_list = pickle.load(todo)


    #Initialize an array to be filled with all correlation values

    # Use a single file to determine in how many bins corr was calculated
    test_file = data_dir + 'MWcorr_' + todo_list[0].ID + '.dat'
    some_column = np.genfromtxt(test_file, unpack = True, usecols = [0])
    N_cols = len(some_column)

    N_rows = len(todo_list)

    data_array = np.zeros((N_rows, N_cols))

    #
    for p in todo_list:
        index = todo_list.index(p)

        # cor_file = data_dir + 'correlation_' + p.ID + '.dat'
        cor_file = data_dir + 'MWcorr_' + p.ID + '.dat'

        if not os.path.isfile(cor_file):
            sys.stderr.write('Warning: ' + cor_file + ' does not exist.\n')
            continue
        if os.path.getsize(cor_file) == 0:
            sys.stderr.write('Warning: ' + cor_file + ' is empty.\n')
            continue

        # read in correlations of each plate
        temp = np.genfromtxt(cor_file, unpack = True, usecols = [1])

        # Each column of data_array contains a list of all (every plate)
        # correlation values for a particular bin.
        for i in range(len(temp)):

            if math.isnan(temp[i]):
                continue

            data_array[index, i] = temp[i]

    # Calculate mean, std, and err for each bin
    mean = np.sum(data_array, axis = 0) / N_rows
    std = (data_array - mean) * (data_array - mean)
    std = np.sum(std, axis = 0) / (N_rows - 1)
    std = np.sqrt(std)
    err = std / math.sqrt(N_rows)

    # Prepare data to be output and output
    out_data = np.column_stack((mean, std))
    out_data = np.column_stack((out_data, err))
    output_file = data_dir + 'stat_data.dat'
    np.savetxt(output_file, out_data)

    sys.stderr.write('Results output to {}. \n'.format(output_file))

if __name__ == '__main__':
    main()