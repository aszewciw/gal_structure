#!/usr/bin/env python

from config import *
import numpy as np

'''
Calculates average, std, and error for correlation for the following:
1) Natural Estimator
2) Landy-Szalay Estimator
3) N.E. - L.S.

'''

def main():

    # load the todo pointing list
    input_filename = data_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    with open(input_filename, 'rb') as todo:
        todo_list = pickle.load(todo)


    #Initialize an array to be filled with all correlation values

    # Use a single file to determine in how many bins corr was calculated
    test_file   = data_dir + 'correlation_' + todo_list[0].ID + '.dat'
    some_column = np.genfromtxt(test_file, unpack = True, usecols = [0])
    N_cols      = len(some_column)
    N_rows      = len(todo_list)

    LS_array    = np.zeros((N_rows, N_cols))
    NE_array    = np.zeros((N_rows, N_cols))


    for p in todo_list:
        index = todo_list.index(p)

        NE_file = data_dir + 'correlation_' + p.ID + '.dat'
        LS_file = corrdata_dir + 'correlation_' + p.ID + '.dat'

        # Check files
        if not os.path.isfile(NE_file):
            sys.stderr.write('Warning: ' + NE_file + ' does not exist.\n')
            continue
        if os.path.getsize(NE_file) == 0:
            sys.stderr.write('Warning: ' + NE_file + ' is empty.\n')
            continue
        if not os.path.isfile(LS_file):
            sys.stderr.write('Warning: ' + LS_file + ' does not exist.\n')
            continue
        if os.path.getsize(LS_file) == 0:
            sys.stderr.write('Warning: ' + LS_file + ' is empty.\n')
            continue

        # read in correlations of each plate
        NE_temp = np.genfromtxt(NE_file, unpack = True, usecols = [1])
        LS_temp = np.genfromtxt(LS_file, unpack = True, usecols = [1])

        # Each column of data_array contains a list of all (every plate)
        # correlation values for a particular bin.
        for i in range(len(NE_temp)):

            if math.isnan(NE_temp[i]):
                continue
            if math.isnan(LS_temp[i]):
                continue

            NE_array[index, i] = NE_temp[i]
            LS_array[index, i] = LS_temp[i]

    # Find differences
    diff_array = NE_array - LS_array

    '''Statistical data for Natural estimator'''
    # Calculate mean, std, and err for each bin
    mean        = np.sum(NE_array, axis = 0) / N_rows
    std         = (NE_array - mean) * (NE_array - mean)
    std         = np.sum(std, axis = 0) / (N_rows - 1)
    std         = np.sqrt(std)
    err         = std / math.sqrt(N_rows)

    # Prepare data to be output and output
    out_data    = np.column_stack((mean, std))
    out_data    = np.column_stack((out_data, err))
    output_file = corrdata_dir + 'NE_stats.dat'
    np.savetxt(output_file, out_data)


    '''Stat data for Landy-Szalay'''
    # Calculate mean, std, and err for each bin
    mean        = np.sum(LS_array, axis = 0) / N_rows
    std         = (LS_array - mean) * (LS_array - mean)
    std         = np.sum(std, axis = 0) / (N_rows - 1)
    std         = np.sqrt(std)
    err         = std / math.sqrt(N_rows)

    # Prepare data to be output and output
    out_data    = np.column_stack((mean, std))
    out_data    = np.column_stack((out_data, err))
    output_file = corrdata_dir + 'LS_stats.dat'
    np.savetxt(output_file, out_data)

    '''Stat data for differences'''
    # Calculate mean, std, and err for each bin
    mean        = np.sum(diff_array, axis = 0) / N_rows
    std         = (diff_array - mean) * (diff_array - mean)
    std         = np.sum(std, axis = 0) / (N_rows - 1)
    std         = np.sqrt(std)
    err         = std / math.sqrt(N_rows)

    # Prepare data to be output and output
    out_data    = np.column_stack((mean, std))
    out_data    = np.column_stack((out_data, err))
    output_file = corrdata_dir + 'Difference_stats.dat'
    np.savetxt(output_file, out_data)

    sys.stderr.write('Results output to {}. \n'.format(output_file))

if __name__ == '__main__':
    main()