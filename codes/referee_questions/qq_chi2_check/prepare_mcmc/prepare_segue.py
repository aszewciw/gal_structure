'''
Get a file of x,y,z for randoms.
'''

from config import *

## ------------------------------------------------------------------------- ##

def line_prepender(filename, line):
    '''
    Appends a line to the beginning of a file.

    Arguments:
    1. filename : (str) name of file
    2. line : (str) line to be appended
    '''
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

## ------------------------------------------------------------------------- ##

def main():

    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    bins_file = rbins_dir + 'rbins.ascii.dat'
    if not os.path.isfile(bins_file):
        sys.stderr.write('Error: ' + bins_file + ' does not exist.\n')

    bin_lower, bin_upper = np.genfromtxt(bins_file, skip_header=1,
        unpack=True, usecols=[0, 1])

    Nbins = len(bin_lower)

    for p in todo_list:

        in_file = qq_dir + 'star_' + p.ID + '.ascii.dat'
        if not os.path.isfile(in_file):
            sys.stderr.write('Error: ' + in_file + ' does not exist.\n')
            continue

        x,y,z,w = np.genfromtxt(in_file, unpack=True, usecols=[7,8,9,10], skip_header=1)
        xy      = np.column_stack((x,y))
        zw      = np.column_stack((z,w))
        xyzw    = np.column_stack((xy,zw))

        outfile = qq_dir + 'star_' + p.ID + '.xyzw.dat'
        np.savetxt(outfile, xyzw)
        N_stars = str(len(xyzw))
        line_prepender(outfile, N_stars)

if __name__ == '__main__':
    main()