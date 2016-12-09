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

        # move nonuniform zrw files
        nonuni_file = nonuni_dir + 'nonuniform_' + p + '.zrw.dat'
        cmd = ('cp ' + nonuni_file + ' ' + zrw_dir)
        os.system(cmd)

        # Repack files containing sigmas
        sigma_file = sigma_dir + 'stats_' + p + '.dat'
        std = np.genfromtxt(sigma_file, unpack=True, usecols=[2])

        outfile = errors_dir + 'fid_std_' + p + '.dat'
        np.savetxt(outfile, std, fmt='%.6f')

if __name__ == '__main__':
    main()
