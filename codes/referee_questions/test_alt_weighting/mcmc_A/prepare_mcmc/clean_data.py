'''
Prepare a couple files for the mcmc:

1. Take todo list and output file containing each pointing ID
2. Take uniform file and output a new file containing only Z, R, and W
3. Output a file containing fractional standard deviation in DD (from 1000 mocks)
'''

from config import *

def main():

    todo_file = rawdata_dir + 'todo_list.ascii.dat'
    ID        = np.genfromtxt(todo_file, unpack=True, skip_header=1,
        usecols=[0], dtype=str)

    # Repack file of just pointing IDs
    outfile   = rawdata_dir + 'pointing_ID.dat'
    with open(outfile, 'w') as f:
        f.write(str(len(ID)))
        f.write('\n')
        for i in range(len(ID)):
            f.write("{}\n".format(ID[i]))


    for p in ID:

        # Repack file containing Z, R, and model weight
        print('On pointing ' + p)
        nonuni_file = uni_dir + 'mock_' + p + '.xyzw.dat'
        x,y,z,w = np.genfromtxt(nonuni_file, unpack=True, skip_header=1)
        N_points = len(x)

        outfile  = zrw_dir + 'uniform_ZRW_' + p + '.dat'
        with open(outfile, 'w') as f:
            f.write(str(N_points))
            f.write('\n')
            for i in range(N_points):
                ra, dec, r = cart2eq(x[i], y[i], z[i])
                l, b = eq2gal(ra, dec)
                Z, R = gal2ZR(l, b, r)
                f.write("{} {} {}\n".format(Z, R, w[i]))

        # Repack files containing sigma/DD
        sigma_file = sigma_dir + 'stats_' + p + '.dat'
        DD, std = np.genfromtxt(sigma_file, unpack=True, usecols=[3,5])
        frac_std = std/DD

        outfile = errors_dir + 'frac_error_' + p + '.dat'
        np.savetxt(outfile, frac_std, fmt='%.6f')

if __name__ == '__main__':
    main()
