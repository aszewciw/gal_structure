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

        # Repack file containing Z, R, and W=1.0 only
        ZRW_file = uni_dir + 'uniform_' + p + '.ascii.dat'
        Z, R, W  = np.genfromtxt(ZRW_file, unpack=True, skip_header=1,
            usecols=[5, 6, 10], dtype=None)
        N_points = len(Z)
        outfile  = zrw_dir + 'uniform_ZRW_' + p + '.dat'
        with open(outfile, 'w') as f:
            f.write(str(N_points))
            f.write('\n')
            for i in range(N_points):
                f.write("{} {} {}\n".format(
                    str(Z[i]), str(R[i]), str(W[i])))

        # Repack files containing sigma/DD
        sigma_file = sigma_dir + 'stats_' + p + '.dat'
        DD, std = np.genfromtxt(sigma_file, unpack=True, usecols=[0,2])
        frac_std = np.zeros(len(DD))
        for i in range(len(DD)):
            if DD[i] == 0.0:
                continue
            frac_std[i] = std[i] / DD[i]

        outfile = errors_dir + 'frac_error_' + p + '.dat'
        np.savetxt(outfile, frac_std, fmt='%.6e')

if __name__ == '__main__':
    main()
