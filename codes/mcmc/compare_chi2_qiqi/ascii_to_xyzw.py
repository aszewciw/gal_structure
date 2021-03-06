'''
Convert Qingqing's ascii files to random xyzw files for pair counting.
Here, w = 1 for the random sample until assigned a weight.
'''

from config import *


def main():

    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    for p in todo_list:

        random_file = qiqi_dir + 'uniform_' + p.ID + '.ascii.dat'

        if not os.path.isfile(random_file):
            sys.stderr.write('Error: ' + random_file + ' does not exist.\n')
            continue

        out_file   = model_dir + 'uniform_' + p.ID + '.xyzw.dat'

        x, y, z, w = np.genfromtxt(random_file, skip_header = 1, unpack = True, usecols = [7, 8, 9, 10])

        xy         = np.column_stack((x,y))
        zw         = np.column_stack((z,w))
        xyzw       = np.column_stack((xy,zw))

        np.savetxt(out_file, xyzw)

if __name__ == '__main__':
    main()