'''
input the xyzw files from our fiducial nonuniform sample; reweight them according
to each model and output a new xyzw file
'''

from config import *
import os, sys
import numpy as np

#--------------------------------------------------------------------------

def gal_weights(Z, R):
    '''
    Returns a weight based on a particular model of the MW.
    For now we will use a two-disk model with the form below.
    This can be expanded at a later time.

    Z - Height above/below galactic plane
    R - Distance from galactic center

    '''

    # Parameters
    thick_s_height = 0.674
    thick_s_length = 2.51
    thin_s_height = 0.283
    thin_s_length = 2.34
    a = 0.1

    weight = ( ( ( math.cosh(Z / 2 / thin_s_height) ) ** (-2) )
        * math.exp(-R / thin_s_length) +
        a * ( ( math.cosh(Z / 2 / thick_s_height) ) ** (-2) )
        * math.exp(-R / thick_s_length))

    return weight


#--------------------------------------------------------------------------
def xyz_to_ZR(x,y,z):

    ra, dec, r = cart2eq(x, y, z)
    l, b = eq2gal(ra, dec)
    Z, R = gal2ZR(l, b, r)

    return Z,R
#--------------------------------------------------------------------------

def main():

    todo_file = rawdata_dir + 'todo_list.ascii.dat'
    ID_list = np.genfromtxt(todo_file, skip_header=1, usecols=[0], unpack=True,
                            dtype=str)
    N_los = len(ID_list)

    for p in ID_list:

        uni_file = uni_dir + 'uniform_' + p + '.xyzw.dat'

        if not os.path.isfile(uni_file):
            sys.stderr.write('Error: ' + uni_file + ' does not exist.\n')
            continue

        nonuni_file = nonuni_dir + 'mock_' + p + '.xyzw.dat'

        if not os.path.isfile(nonuni_file):
            sys.stderr.write('Error: ' + nonuni_file + ' does not exist.\n')
            continue

        x_u, y_u, z_u, w_u = np.genfromtxt(uni_file, skip_header=1, unpack=True)
        x_n, y_n, z_n, w_n = np.genfromtxt(nonuni_file, skip_header=1, unpack=True)

        w_u_new = np.zeros(len(x_u))
        w_n_new = np.zeros(len(x_u))

        for i in range(len(x_u)):

            Z_u, R_u = xyz_to_ZR(x_u[i],y_u[i],z_u[i])
            Z_n, R_n = xyz_to_ZR(x_n[i],y_n[i],z_n[i])
            w_u_new[i] = gal_weights(Z_u, R_u)
            w_n_new[i] = gal_weights(Z_n, R_n) / w_n[i]

        # output xyzw
        output_filename = data_dir + 'nonuni_reweighted_'+ p + '.xyzw.dat'
        output_file = open(output_filename, "w")
        output_file.write('{}\n'.format(len(x_u)))
        for i in range(len(x_u)):
            output_file.write('{0:.6e}\t{1:.6e}\t{2:.6e}\t{3:.6e}\n'
                              .format(x_n[i], y_n[i], z_n[i], w_n_new[i]))
        output_file.close()

        output_filename = data_dir + 'uni_reweighted_'+ p + '.xyzw.dat'
        output_file = open(output_filename, "w")
        output_file.write('{}\n'.format(len(x_u)))
        for i in range(len(x_u)):
            output_file.write('{0:.6e}\t{1:.6e}\t{2:.6e}\t{3:.6e}\n'
                              .format(x_u[i], y_u[i], z_u[i], w_u_new[i]))
        output_file.close()
if __name__ == '__main__':
    main()