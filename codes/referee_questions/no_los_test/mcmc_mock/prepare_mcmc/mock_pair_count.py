'''
Loops over all SEGUE los and produces a file for each
mock containing the normalized dd counts.
'''

from config import *

def main():

    bins_file = rbins_dir + 'rbins.ascii.dat'
    if not os.path.isfile(bins_file):
        sys.stderr.write('Error: ' + bins_file + ' does not exist.\n')

    in_file = mock_dir + 'mock_xyz.dat'

    if not os.path.isfile(in_file):
        sys.stderr.write('Error: ' + in_file + ' does not exist.\n')
        continue

    output_file = mock_dd_dir + 'dd.dat'

    cmd = ( './mock_pair_count ' + in_file + ' ' + bins_file + ' > '
        + output_file )
    os.system(cmd)

if __name__ == '__main__':
    main()