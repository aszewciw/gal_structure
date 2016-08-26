#!/usr/bin/env python

import sys, math, pickle
import config

#------------------------------------------------------------------------------
def main():

    # load pointing list
    input_filename = config.data_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file = open(input_filename, 'rb')
    todo_list = pickle.load(input_file)
    input_file.close()

    sys.stderr.write('Prepare data files for correlation function calculation..\n')

    N_tot = 0

    for p in todo_list:

        star_filename = config.rawdata_dir + 'star_' + p.ID + '.dat'
        star_file = open(star_filename, 'rb')
        star_list = pickle.load(star_file)
        star_file.close()

        N_tot += len(star_list)

    N_tot2 = sum([p.N_star for p in todo_list])

    print len(todo_list), N_tot, N_tot2

if __name__ == '__main__' :
    main()





