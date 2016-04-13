#!/usr/bin/env python

from config import *

#------------------------------------------------------------------------------
def main():

    thin_file = './out_data/thin_disk_smallmock.npz'
    with np.load(thin_file) as d:
        x_thin = d['x_thin']
        y_thin = d['y_thin']
        z_thin = d['z_thin']
        ra_thin = d['ra_thin']
        dec_thin = d['dec_thin']

    thick_file = './out_data/thick_disk_smallmock.npz'
    with np.load(thick_file) as d:
        x_thick = d['x_thick']
        y_thick = d['y_thick']
        z_thick = d['z_thick']
        ra_thick = d['ra_thick']
        dec_thick = d['dec_thick']

    # Pack stars together...it really doesn't matter to what disk they belong
    x   = np.append(x_thin, x_thick)
    y   = np.append(y_thin, y_thick)
    z   = np.append(z_thin, z_thick)
    ra  = np.append(ra_thin, ra_thick)
    dec = np.append(dec_thin, dec_thick)

    input_filename = 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    pointing_list  = pickle.load(input_file)
    input_file.close()

    # the cos of the plate size
    plate_size_cos = math.cos(PLATE_RADIUS_RADIANS)

    # For each star in the photometric sample, check which pointing it belongs
    # to, and assign the corresponding pointing ID to it.
    status_count = 0

    N_stars = len(x)

    print(N_stars)

    for p in pointing_list:
        p.star_list = []

    for i in range(N_stars):
        s_cart = (x[i], y[i], z[i])
        s_xyz = eq2cart(ra[i], dec[i], 1.0)
        for p in pointing_list:
            # get star's Cartesian coordinates on the unit sphere
            p_xyz = (p.cartesian_x, p.cartesian_y, p.cartesian_z)
            if dot(s_xyz, p_xyz) >= plate_size_cos:
                # s.pointingID = p.ID
                p.star_list.append(s_cart)
                break

    sys.stderr.write('Start splitting files...\n')

    count = 0
    # open files and output for each pointing:
    for p in pointing_list:

        if len(p.star_list) == 0:
            continue # skip empty or very few stars pointing
        print(len(p.star_list))
        count += 1
        xyz = np.asarray(p.star_list)
        output_filename = './data/mock_raw_' + p.ID + '.dat'
        np.savetxt(output_filename, xyz)

    print(count)
    sys.stderr.write("Done splitting files.\n")

if __name__ == '__main__':
    main()