from config import *
# ---------------------------------------------------------------------------- #

'''
Output a file containing evenly spaced values of r from
the inner distance to the outer distance of our sample.

CL Input for number of bins.
'''
# ---------------------------------------------------------------------------- #

def get_volume(r1, r2, plate_radius):

    '''
    For a SEGUE pointing, get the volume betweeen r1 and r2.

    r1:             numpy array of inner distance limit
    r2:             numpy array of outer distance limit
    plate_radius:   radius of plate in radians
    '''

    # get the steradians by doing a pseudo integration in spherical coordinates

    # Integral of sin(theta)*dtheta from 0 to plate radius
    theta_int = 1.0 - math.cos(plate_radius)

    # Integral of dphi from 0 to 2pi
    phi_int = 2.0*math.pi

    # Steradian fraction of whole sky
    str_fraction = theta_int*phi_int / (4.0*math.pi)

    # Volumes of full spheres with radius equal to inner and outer radii
    vol_inner = (4.0/3.0)*np.pi*r1**3
    vol_outer = (4.0/3.0)*np.pi*r2**3

    # Volume of bin
    volume = str_fraction * (vol_outer - vol_inner)

    return volume

# ---------------------------------------------------------------------------- #
def main():

    # CL input of number of bins
    elements_needed = int(2)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args   == elements_needed)
    Nbins           = int(args_array[1])

    # Make evenly spaced array of r-values
    r_bins = np.linspace(INNER_DISTANCE_LIMIT, OUTER_DISTANCE_LIMIT, Nbins+1)

    # Define inner and outer limit of each radial bin
    r_mins = np.delete(r_bins, -1)
    r_maxs = np.delete(r_bins, 0)

    # Array of volumes for each bin
    vol = get_volume(r_mins, r_maxs, PLATE_RADIUS_RADIANS)

    # Output file with limits and volumes
    out_file = data_dir + 'rbins.dat'

    with open(out_file, 'w') as f:
        f.write(str(Nbins))
        f.write('\n')
        for i in range(Nbins):
            f.write( '{}\t{}\t{}\n'.format(r_mins[i], r_maxs[i], vol[i]) )


if __name__ == '__main__':
    main()