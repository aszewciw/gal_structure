'''
Loops over all SEGUE los and produces a file for each los
(152) of the weighted and weighted and normalized data
pair counts in each bin.
'''

from config import *

def main():

    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    for p in todo_list:

        in_file = xyzw_dir + 'star_' + p.ID + '.xyzw.dat'

        if not os.path.isfile(in_file):
            sys.stderr.write('Error: ' + in_file + ' does not exist.\n')
            continue

        param = str(bin_min) + ' ' + str(bin_max) + ' ' + str(Nbins)

        output_file = DD_dir + 'DD_' + p.ID + '.dat'

        cmd = './data_pair_count ' + in_file + ' ' + param + ' > ' + output_file

        os.system(cmd)

if __name__ == '__main__':
    main()