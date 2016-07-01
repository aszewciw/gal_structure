'''
Calculate mock density and Poisson error in calculation.
'''
from config import *

def main():

    # load the todo pointing list
    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    for p in todo_list:

        # a progress indicator
        if todo_list.index(p) % 10 == 0:
            sys.stderr.write('On pointing #{} of {} ..\n'
                             .format(todo_list.index(p), len(todo_list)))

        error_file = stats_dir + 'ave_std_' + p.ID + '.dat'
        stdev = np.genfromtxt(error_file, unpack=True, usecols=[1])

        output_file = errors_dir + 'errors_' + p.ID + '.dat'

        np.savetxt(output_file, stdev)


if __name__ == '__main__':
    main()