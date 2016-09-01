'''
Convert Qingqing's ascii files to random xyzw files for pair counting.
Here, w = 1 for the random sample until assigned a weight.
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

def main():

    input_filename = todo_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    for p in todo_list:

        random_file = uni_dir + 'uniform_' + p.ID + '.ascii.dat'

        if not os.path.isfile(random_file):
            sys.stderr.write('Error: ' + random_file + ' does not exist.\n')
            continue

        out_file   = uni_dir + 'uniform_' + p.ID + '.xyz.dat'

        x, y, z = np.genfromtxt(random_file, skip_header = 1, unpack = True, usecols = [7, 8, 9])

        xy  = np.column_stack((x,y))
        xyz = np.column_stack((xy,z))

        np.savetxt(out_file, xyz)
        N_stars = str(len(x))

        line_prepender(out_file, N_stars)

if __name__ == '__main__':
    main()