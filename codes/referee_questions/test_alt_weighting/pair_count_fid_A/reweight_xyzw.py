'''
input the xyzw files from our fiducial nonuniform sample; reweight them according
to each model and output a new xyzw file
'''

from config import *
import os, sys
import numpy as np

#--------------------------------------------------------------------------

def gal_weights(Z, R, model):
    '''
    Returns a weight based on a particular model of the MW.
    For now we will use a two-disk model with the form below.
    This can be expanded at a later time.

    Z - Height above/below galactic plane
    R - Distance from galactic center

    '''

    if model=='A':
        # Parameters
        thick_s_height = 0.674
        thick_s_length = 2.51
        thin_s_height = 0.233
        thin_s_length = 2.34
        a = 0.1
    elif model=='B':
        # Parameters
        thick_s_height = 0.8
        thick_s_length = 4.0
        thin_s_height = 0.4
        thin_s_length = 3.0
        a = 0.2
    elif model=='C':
        # Parameters
        thick_s_height = 0.72
        thick_s_length = 2.8
        thin_s_height = 0.2
        thin_s_length = 2.1
        a = 0.08
    else:
        raise ValueError('Input model A, B, or C')


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

    fiducial_dir = A_nonuni_dir

    todo_file = rawdata_dir + 'todo_list.ascii.dat'
    ID_list = np.genfromtxt(todo_file, skip_header=1, usecols=[0], unpack=True,
                            dtype=str)
    N_los = len(ID_list)

    for p in ID_list:

        fid_file = fiducial_dir + 'mock_' + p + '.xyzw.dat'

        if not os.path.isfile(fid_file):
            sys.stderr.write('Error: ' + in_file + ' does not exist.\n')
            continue

        x,y,z,w = np.genfromtxt(fid_file, skip_header=1, unpack=True)

        w_A = np.zeros(len(x))
        w_B = np.zeros(len(x))
        w_C = np.zeros(len(x))

        for i in range(len(x)):

            Z, R = xyz_to_ZR(x[i],y[i],z[i])
            w_A[i] = gal_weights(Z,R,'A')
            w_B[i] = gal_weights(Z,R,'B')
            w_C[i] = gal_weights(Z,R,'C')

        # output xyzw
        output_filename = data_dir + 'nonuni_reweighted_A_'+ p + '.xyzw.dat'
        output_file = open(output_filename, "w")
        output_file.write('{}\n'.format(len(x)))
        for i in range(len(x)):
            # output_file.write('{}\t{}\t{}\t{}\n'
            output_file.write('{0:.6e}\t{1:.6e}\t{2:.6e}\t{3:.6e}\n'
                              .format(x[i], y[i], z[i], w_A[i]))
        output_file.close()

        # output xyzw
        output_filename = data_dir + 'nonuni_reweighted_B_'+ p + '.xyzw.dat'
        output_file = open(output_filename, "w")
        output_file.write('{}\n'.format(len(x)))
        for i in range(len(x)):
            # output_file.write('{}\t{}\t{}\t{}\n'
            output_file.write('{0:.6e}\t{1:.6e}\t{2:.6e}\t{3:.6e}\n'
                              .format(x[i], y[i], z[i], w_B[i]))
        output_file.close()

        # output xyzw
        output_filename = data_dir + 'nonuni_reweighted_C_'+ p + '.xyzw.dat'
        output_file = open(output_filename, "w")
        output_file.write('{}\n'.format(len(x)))
        for i in range(len(x)):
            # output_file.write('{}\t{}\t{}\t{}\n'
            output_file.write('{0:.6e}\t{1:.6e}\t{2:.6e}\t{3:.6e}\n'
                              .format(x[i], y[i], z[i], w_C[i]))
        output_file.close()

if __name__ == '__main__':
    main()