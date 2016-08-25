'''
Reads in the data files of random points, weights them
to match a particular Milky way model, and outputs files.
Data input and output is x, y, z, and weight.
'''

from config import *

def gal_weights(Z, R):
    '''
    Returns a weight based on a particular model of the MW.
    For now we will use a two-disk model with the form below.
    This can be expanded at a later time.

    Z - Height above/below galactic plane
    R - Distance from galactic center

    '''

    # Parameters
    z0_thick = 0.674
    r0_thick = 2.51
    z0_thin  = 0.233
    r0_thin  = 2.34
    a        = 0.1

    # try min chi2 of mcmc chain
    # z0_thin  = 0.248627
    # r0_thin  = 2.725662
    # z0_thick = 0.684135
    # r0_thick = 2.201223
    # a        = 0.378596

    # try min chi2 of chain when a is held at 0.1
    # z0_thin  = 0.25273
    # r0_thin  = 1.774479
    # z0_thick = 0.686907
    # r0_thick = 2.066177
    # a        = 0.1

    # min for more dense
    # z0_thin = 0.252392
    # r0_thin = 1.778989
    # z0_thick = 0.67459
    # r0_thick = 1.872601
    # a = 0.149975

    # other params
    # z0_thin = 0.8
    # r0_thin = 4
    # z0_thick = 1
    # r0_thick = 3
    # a = 0.3

    # weight = ( ( ( math.cosh(Z / 2 / z0_thin) ) ** (-2) )
    #     * math.exp(-R / r0_thin) +
    #     a * ( ( math.cosh(Z / 2 / z0_thick) ) ** (-2) )
    #     * math.exp(-R / r0_thick) )

    # Try alternate weighting according to #, not # density
    thin_weight = ( r0_thin * math.exp(-R/r0_thin) * (r0_thin + R)
        * 2 * z0_thin * math.tanh(math.fabs(Z)/(2*z0_thin)) )
    thick_weight = ( r0_thick * math.exp(-R/r0_thick) * (r0_thick + R)
        * 2 * z0_thick * math.tanh(math.fabs(Z)/(2*z0_thick)) )

    weight = thin_weight + a * thick_weight

    return weight

def main():

    input_file = rawdata_dir + 'todo_list.dat'

    with open(input_file, 'rb') as data:
        todo_list = pickle.load(data)

    for p in todo_list:

        rand_file = uniform_dir + 'uniform_' + p.ID + '.xyz.dat'

        if not os.path.isfile(rand_file):

            sys.stderr.write('Error: ' + rand_file
                + ' does not exist.\n')
            continue

        output_file = data_dir + 'MWM_' + p.ID + '.xyzw.dat'

        x, y, z = np.genfromtxt(rand_file, skip_header=1, unpack=True)

        ra, dec, r = np.zeros(len(x)), np.zeros(len(x)), np.zeros(len(x))
        l, b = np.zeros(len(x)), np.zeros(len(x))
        Z, R = np.zeros(len(x)), np.zeros(len(x))

        w = np.zeros(len(x))

        for i in range(len(x)):
            ra[i], dec[i], r[i] = cart2eq(x[i], y[i], z[i])
            l[i], b[i] = eq2gal(ra[i], dec[i])
            Z[i], R[i] = gal2ZR(l[i], b[i], r[i])
            w[i] = gal_weights(Z[i], R[i])

        xyzw = np.column_stack((x, y))
        xyzw = np.column_stack((xyzw, z))
        xyzw = np.column_stack((xyzw, w))

        np.savetxt(output_file, xyzw)


if __name__ == '__main__':
    main()
