from config import *

'''
Make uniform density points within a sphere of radius r_max
'''
#------------------------------------------------------------------------------

def get_random_distance(N, rmax):
    '''
    Generate distances uniformly from center to rmax
    '''

    # Normalize pdf by integrating from 0 to rmax
    pdf_norm = 1.0 / (rmax**3 / 3.0)

    # Draw N random values between 0 and 1
    cdf = np.random.rand(N)

    # Invert cdf equation to get random r
    distance = ( cdf / (pdf_norm / 3.0) )**(1.0/3.0)

    return distance


#------------------------------------------------------------------------------
def get_random_theta(N):
    '''
    Generate values of theta uniformly within sphere
    '''

    # Integrate from 0 to pi to normalize
    pdf_norm = 0.5

    # Draw N random values between 0 and 1
    cdf = np.random.rand(N)

    #invert cdf to get theta
    angle = np.arccos(1.0 - cdf/pdf_norm)

    return angle

#------------------------------------------------------------------------------

def main():

    # Check for correct number of arguments passed in CL
    elements_needed = int(3)
    args_array = np.array(sys.argv)
    N_args = len(args_array)
    assert(N_args == elements_needed)

    # Assign CL arguments
    N_data = int(args_array[1])     # stars in data sample
    factor = int(args_array[2])     # how many times more stars in rand sample

    N_random = factor * N_data

    r_max = OUTER_DISTANCE_LIMIT

    # Seed random
    np.random.seed()

    # Generate uniform points within a sphere
    r     = get_random_distance(N_random, r_max)
    phi   = 2.0 * np.pi * np.random.rand(N_random)
    theta = get_random_theta(N_random)

    # Do spherical to cartesian conversion
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)

    # Get other coordinates
    ra, dec = cart2eq(x, y, z)
    l, b    = eq2gal(ra, dec)
    Z, R    = gal2ZR(l, b, r)

    filename = data_dir + 'random_all.dat'
    sys.stderr.write('Writing file containing all data...\n')

    with open(filename, 'w') as f:
        f.write(str(N_random))
        f.write('\n')
        for i in range(N_random):
            f.write("{} {} {} {} {} {} {} {} {}\n".format(
                str(x[i]), str(y[i]), str(z[i]), str(ra[i]), str(dec[i]),
                str(l[i]), str(b[i]), str(Z[i]), str(R[i])))

    filename = data_dir + 'random_xyz.dat'
    sys.stderr.write('Writing file containing xyz data...\n')

    with open(filename, 'w') as f:
        f.write(str(N_random))
        f.write('\n')
        for i in range(N_random):
            f.write("{} {} {}\n".format(str(x[i]), str(y[i]), str(z[i])))

    filename = data_dir + 'random_ZR.dat'
    sys.stderr.write('Writing file containing ZR data...\n')

    with open(filename, 'w') as f:
        f.write(str(N_random))
        f.write('\n')
        for i in range(N_random):
            f.write("{} {}\n".format(str(Z[i]), str(R[i])))



if __name__ == '__main__':
    main()