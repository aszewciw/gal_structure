from config import *

def main():

    input_file = rawdata_dir + 'todo_list.dat'

    with open(input_file, 'rb') as data:
        todo_list = pickle.load(data)

    for p in todo_list:

        mock_file = data_dir + 'mock_' + p.ID + '.xyz.dat'

        if not os.path.isfile(mock_file):
            sys.stderr.write('Error: ' + mock_file
                + ' does not exist.\n')
            continue

        x, y, z = np.genfromtxt(mock_file, skip_header=1, unpack=True)

        N = len(x)
        w = np.ones(N)
        xyzw = np.column_stack((x, y))
        xyzw = np.column_stack((xyzw, z))
        xyzw = np.column_stack((xyzw, w))

        output_file = data_dir + 'mock_' + p.ID + '.xyzw.dat'
        np.savetxt(output_file, xyzw)


if __name__ == '__main__':
    main()