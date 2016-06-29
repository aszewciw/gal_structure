
'''
As I'm working on this HPC project, I want to clean some
files so I have the following things:

1. File containing just pointing IDs
2. Files containing just Z, R, W, for uniform points
3. Files containing just the fractional errors

There is no need to overload my data structures with
things I'll never use in the MCMC.
This is a bit sloppy of a way to do this all, but for now
my main concern is getting my mcmc to work. After that, I
will work on data preparation files.
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

        # Repack uniform error files
        uni_jk_file = jk_dir + 'uniform_' + p + '_jk_error.dat'
        uni_jk_err  = np.genfromtxt(uni_jk_file, unpack=True, usecols=[7])
        outfile     = errors_dir + 'uniform_' + p + '_frac_error.dat'
        np.savetxt(outfile, uni_jk_err)

        # Repack mock error files
        # Get a fractional error so we don't have to change mcmc code
        mock_sigma_file = sigma_dir + 'stats_' + p + '.dat'
        mock_sigma = np.genfromtxt(mock_sigma_file, unpack=True,
            usecols = [2])
        dd_file = mock_dd_dir + 'dd_' + p + '.dat'
        dd      = np.genfromtxt(dd_file)

        mock_frac_error = np.zeros(len(dd))

        for i in range(len(dd)):

            # skip if either is 0 and ignore in chi2 calc
            if dd[i]==0 or mock_sigma[i]==0:
                continue
            mock_frac_error[i] = mock_sigma[i] / dd[i]

        outfile = errors_dir + 'mock_' + p + '_frac_error.dat'
        np.savetxt(outfile, mock_frac_error)


if __name__ == '__main__':
    main()
