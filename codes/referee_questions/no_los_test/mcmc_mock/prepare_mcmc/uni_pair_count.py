'''
Loops over all SEGUE los and produces a file for each bin (12)
in each los (152) containing the indices of pairs in a uniform
sample with same geometry as that los.
'''

from config import *

#-------------------------------------------------------------------------

def main():

    bins_file = rbins_dir + 'rbins.ascii.dat'
    if not os.path.isfile(bins_file):
        sys.stderr.write('Error: ' + bins_file + ' does not exist.\n')

    bin_lower, bin_upper = np.genfromtxt(bins_file, skip_header=1,
        unpack=True, usecols=[0, 1])

    Nbins = len(bin_lower)

    in_file = uni_dir + 'random_' + p.ID + '.xyz.dat'
    if not os.path.isfile(in_file):
        sys.stderr.write('Error: ' + in_file + ' does not exist.\n')
        continue

    # Count pairs in each bin
    for i in range(Nbins):

        param = str(bin_lower[i]) + ' ' + str(bin_upper[i])
        output_file = pairs_dir + 'counts_bin_' + str(i) + '.dat'
        cmd = ( './uni_pair_count ' + in_file + ' ' + param + ' > '
            + output_file )
        os.system(cmd)

        # prepend length of array to file
        indexes = np.genfromtxt(output_file)
        length  = str(len(indexes))
        line_prepender(output_file, length)

if __name__ == '__main__':
    main()