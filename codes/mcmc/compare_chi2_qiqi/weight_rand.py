'''
Reads in random xyzw with same number of points as each
SEGUE los, and assigns a new weight based on a model.
This new xyzw is to be used to test mymcmc
'''

from config import *


#############################################################

def gal_weights(Z, R, r_thin, r_thick, z_thin, z_thick, a):

    '''
    For numpy arrays of (Z,R) values of different star,
    calculates the "weight" of each star based on the 5
    parameters.
    '''

    # Min chi2 results from /fs1/szewciw/gal_structure/codes/mcmc/compare_chi2_qiqi/debugging_March/data/mcmc_2disks_model.dat
    # Min params were found from the mcmc_result.dat file in qiqi_dir
    # As a side note, the chi2 value he measured was ~2860; it can be found in the above file
    # r_thin  = 2.02695
    # z_thin  = 0.233619
    # r_thick = 2.3965745
    # z_thick = 0.674525
    # a       = 0.052944

    weight = ( ( ( np.cosh(Z / 2 / z_thin) ) ** (-2) )
        * np.exp(-R / r_thin) +
        a * ( ( np.cosh(Z / 2 / z_thick) ) ** (-2) )
        * np.exp(-R / r_thick) )

    return weight

#############################################################

def main():

    elements_needed = int(2)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args   == elements_needed)
    infile          = args_array[1]
    infile          = chi2min_dir + infile

    chi2_qiqi, r_thin, z_thin, r_thick, z_thick, a = np.genfromtxt(infile, unpack=True)

    print("Expected minimum chi2 is ", chi2_qiqi)


    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    for p in todo_list:

        random_file = model_dir + 'uniform_' + p.ID + '.xyzw.dat'

        if not os.path.isfile(random_file):
            sys.stderr.write('Error: ' + random_file + ' does not exist.\n')
            continue

        out_file   = weighted_dir + 'weighted_' + p.ID + '.xyzw.dat'

        x, y, z = np.genfromtxt(random_file, skip_header = 1, unpack = True, usecols=[0,1,2])

        # All my config equations are very unfortunately not set up to take in np arrays
        # And I don't feel like changing them.

        N = len(x)

        r, ra, dec, l, b, Z, R = np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N)

        for i in range(N):
            ra[i], dec[i], r[i] = cart2eq(x[i], y[i], z[i])
            l[i], b[i]          = eq2gal(ra[i], dec[i])
            Z[i], R[i]          = gal2ZR(l[i], b[i], r[i])

        weight = gal_weights(Z, R, r_thin, r_thick, z_thin, z_thick, a)

        xy     = np.column_stack((x,y))
        zw     = np.column_stack((z, weight))
        xyzw   = np.column_stack((xy,zw))

        np.savetxt(out_file, xyzw)


if __name__ == '__main__':
    main()