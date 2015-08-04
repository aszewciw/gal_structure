#!/usr/bin/env python

from config import *

def main():

    # load the todo pointing list
    input_filename = data_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file = open(input_filename, 'r')
    todo_list = pickle.load(input_file)
    input_file.close()

    output_filename = plots_dir + 'correlation.plt.tmp'
    output_file = open(output_filename, 'w')

    for p in todo_list:
        output_file.write('\t"' + data_dir + 'correlation_' + p.ID + '.dat" u 1:2 w l lt 1 lw 0.1 lc rgb "gray", \\\n')

    output_file.close()
    sys.stderr.write('Output to {} . \n'.format(output_filename))


if __name__ == '__main__' :
    main()

