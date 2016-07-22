from config import *

#------------------------------------------------------------------------------#
'''
A rather stupid file that removes the weight so I can use the same c file for
pair counting.
'''
#------------------------------------------------------------------------------#

def main():

    # load pointing list
    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    for p in todo_list:

        data_filename = segue_dir + 'star_' + p.ID + '.xyzw.dat'
        x,y,z = np.genfromtxt( data_filename, skip_header=1, unpack=True,
                                usecols=[0,1,2] )

        # put together x,y,z
        xy  = np.column_stack((x,y))
        xyz = np.column_stack((xy,z))

        out_filename = segue_dir + 'star_' + p.ID + '.xyz.dat'
        np.savetxt(out_filename, xyz)

        N_stars = str(len(xyz))

        line_prepender(out_filename, N_stars)


if __name__ == '__main__':
    main()

