
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

        # # Repack file containing Z, R, and W=1.0 only
        ZRW_file = model_dir + 'model_' + p + '.ascii.dat'
        Z, R, W  = np.genfromtxt(ZRW_file, unpack=True, skip_header=1,
            usecols=[5, 6, 10], dtype=None)
        N_points = len(Z)
        outfile  = zrw_dir + 'model_ZRW_' + p + '.dat'
        with open(outfile, 'w') as f:
            f.write(str(N_points))
            f.write('\n')
            for i in range(N_points):
                f.write("{} {} {}\n".format(
                    str(Z[i]), str(R[i]), str(W[i])))

if __name__ == '__main__':
    main()
