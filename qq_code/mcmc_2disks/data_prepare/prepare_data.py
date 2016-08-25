#!/usr/bin/env python

import sys, math, pickle
import config

#------------------------------------------------------------------------------
def main():

    # load pointing list
    input_filename = config.data_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file = open(input_filename, 'r')
    todo_list = pickle.load(input_file)
    input_file.close()

    sys.stderr.write('Prepare data files for correlation function calculation..\n')
    
    for p in todo_list:

        star_filename = config.rawdata_dir + 'star_' + p.ID + '.dat'
        star_file = open(star_filename, 'r')
        star_list = pickle.load(star_file)
        star_file.close()

        # output ascii file for correlation function calculation
        output_filename = config.data_dir + 'star_' + p.ID + '.ascii.dat'
        output_file = open(output_filename, 'w')
        # first output the total number of points
        output_file.write('{}\n'.format(len(star_list)))
        for i in star_list:
            output_file.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'
                              .format(i.ra_rad, i.dec_rad, i.distance, 
                                      i.galactic_l_rad, i.galactic_b_rad, 
                                      i.galactic_Z, i.galactic_R,
                                      i.cartesian_x, i.cartesian_y, i.cartesian_z, 
                                      i.weight))
        output_file.close()
    

if __name__ == '__main__' :
    main()


    


