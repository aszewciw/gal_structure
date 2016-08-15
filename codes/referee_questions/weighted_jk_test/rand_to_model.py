'''
Reads in the data files of random points, weights them
to match a particular Milky way model, and outputs files.
Data input and output is x, y, z, and weight.
'''

from config import *
import numpy as np

def gal_weights(Z, R, model):
    '''
    Returns a weight based on a particular model of the MW.
    For now we will use a two-disk model with the form below.
    This can be expanded at a later time.

    Z - Height above/below galactic plane
    R - Distance from galactic center

    '''

    # Parameters
    if model==0:
        thick_s_height = 0.674
        thick_s_length = 2.51
        thin_s_height  = 0.233
        thin_s_length  = 2.34
        a              = 0.1
    elif model==1:
        thick_s_height = 0.8
        thick_s_length = 4.0
        thin_s_height  = 0.3
        thin_s_length  = 3.0
        a              = 0.2


    weight = ( ( ( math.cosh(Z / 2.0 / thin_s_height) ) ** (-2) )
        * math.exp(-R / thin_s_length) +
        a * ( ( math.cosh(Z / 2.0 / thick_s_height) ) ** (-2) )
        * math.exp(-R / thick_s_length))

    return weight

def main():

    elements_needed = int(2)

    args_array = np.array(sys.argv)
    N_args = len(args_array)
    assert(N_args == elements_needed)
    model = int(args_array[1])

    input_file = rawdata_dir + 'todo_list.dat'

    with open(input_file, 'rb') as data:
        todo_list = pickle.load(data)

    for p in todo_list:

        rand_file = uniform_dir + 'uniform_' + p.ID + '.xyz.dat'

        if not os.path.isfile(rand_file):

            sys.stderr.write('Error: ' + rand_file
                + ' does not exist.\n')
            continue

        output_file = out_dir + 'MWM_type' + str(model) + '_' + p.ID + 'xyzw.dat'

        x, y, z = np.genfromtxt(rand_file, skip_header=1, unpack=True)

        ra, dec, r = np.zeros(len(x)), np.zeros(len(x)), np.zeros(len(x))
        l, b = np.zeros(len(x)), np.zeros(len(x))
        Z, R = np.zeros(len(x)), np.zeros(len(x))

        for i in range(len(x)):
            ra[i], dec[i], r[i] = cart2eq(x[i], y[i], z[i])
            l[i], b[i] = eq2gal(ra[i], dec[i])
            Z[i], R[i] = gal2ZR(l[i], b[i], r[i])
            w[i] = gal_weights(Z[i], R[i], model)

        xyzw = np.column_stack((x, y))
        xyzw = np.column_stack((xyzw, z))
        xyzw = np.column_stack((xyzw, w))

        np.savetxt(output_file, xyzw)


if __name__ == '__main__':
    main()
