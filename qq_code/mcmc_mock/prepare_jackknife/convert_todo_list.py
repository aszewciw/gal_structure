#!/usr/bin/env python

from config import *

def main():

    # load todo pointing list
    input_filename = todo_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file = open(input_filename, 'rb')
    todo_list = pickle.load(input_file)
    input_file.close()


    output_filename = todo_dir + 'todo_list.ascii.dat'
    output_file = open(output_filename, "w")

    # first output total number of pointings
    output_file.write('{}\n'.format(len(todo_list)))

    for p in todo_list:
        output_file.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'
                          .format(p.ID, p.ra_deg, p.dec_deg, p.ra_rad, p.dec_rad,
                                  p.galactic_l_rad, p.galactic_b_rad,
                                  p.cartesian_x, p.cartesian_y, p.cartesian_z,
                                  p.N_star))

    output_file.close()
    sys.stderr.write('Output to {} .\n'.format(output_filename))

if __name__ == '__main__' :
    main()


