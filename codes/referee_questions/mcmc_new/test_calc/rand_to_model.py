'''
Reads in the data files of random points, weights them
to match a particular Milky way model, and outputs files.
Data input and output is x, y, z, and weight.
'''

from config import *

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

def gal_weights(Z, R):
    '''
    Returns a weight based on a particular model of the MW.
    For now we will use a two-disk model with the form below.
    This can be expanded at a later time.

    Z - Height above/below galactic plane
    R - Distance from galactic center

    '''

    # Parameters
    thick_s_height = 0.674
    thick_s_length = 2.51
    thin_s_height = 0.233
    thin_s_length = 2.34
    a = 0.10


    weight = ( ( ( math.cosh(Z / 2 / thin_s_height) ) ** (-2) )
        * math.exp(-R / thin_s_length) +
        a * ( ( math.cosh(Z / 2 / thick_s_height) ) ** (-2) )
        * math.exp(-R / thick_s_length))

    return weight

def main():

    input_file = rawdata_dir + 'todo_list.dat'

    with open(input_file, 'rb') as data:
        todo_list = pickle.load(data)

    for p in todo_list:

        rand_file = uni_dir + 'uniform_' + p.ID + '.ascii.dat'

        if not os.path.isfile(rand_file):

            sys.stderr.write('Error: ' + rand_file
                + ' does not exist.\n')

            continue

        output_file = data_dir + 'MWM_' + p.ID + '.dat'

        Z, R, x, y, z, w = np.genfromtxt(rand_file, unpack=True, skip_header=1,
            usecols=[5,6,7,8,9,10])


        # ra, dec, r = np.zeros(len(x)), np.zeros(len(x)), np.zeros(len(x))
        # l, b = np.zeros(len(x)), np.zeros(len(x))
        # Z, R = np.zeros(len(x)), np.zeros(len(x))

        for i in range(len(x)):
            w[i] = gal_weights(Z[i], R[i])

        xyzw = np.column_stack((x, y))
        xyzw = np.column_stack((xyzw, z))
        xyzw = np.column_stack((xyzw, w))

        np.savetxt(output_file, xyzw)
        line_prepender(output_file, str(len(x)))


if __name__ == '__main__':
    main()
