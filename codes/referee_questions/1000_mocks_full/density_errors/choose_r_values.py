from config import *

'''
Output a file containing evenly spaced values of r from
the inner distance to the outer distance of our sample.

CL Input for number of bins.
'''

def get_volume(r1, r2, radius):

    # get the steradians by doing a pseudo integration
    cos_int = 1.0 - math.cos(radius)

    str_fraction = 2.0*math.pi*cos_int / (4.0*math.pi)

    vol_outer = (4.0/3.0)*np.pi*r2**3
    vol_inner = (4.0/3.0)*np.pi*r1**3

    volume = str_fraction * (vol_outer - vol_inner)
    return volume

def main():

    # CL input of number of bins
    elements_needed = int(2)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args   == elements_needed)
    Nbins           = int(args_array[1])

    r_bins = np.linspace(INNER_DISTANCE_LIMIT, OUTER_DISTANCE_LIMIT,
        Nbins+1)

    r_mins = np.delete(r_bins, -1)
    r_maxs = np.delete(r_bins, 0)

    vol = get_volume(r_mins, r_maxs, PLATE_RADIUS_RADIANS)

    out_file = data_dir + 'rbins.dat'

    with open(out_file, 'w') as f:
        f.write(str(Nbins))
        f.write('\n')
        for i in range(Nbins):
            f.write( '{}\t{}\t{}\n'.format(r_mins[i], r_maxs[i], vol[i]) )


if __name__ == '__main__':
    main()