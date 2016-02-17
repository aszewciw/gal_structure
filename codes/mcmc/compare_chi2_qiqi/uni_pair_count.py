'''
Loops over all SEGUE los and produces a file for each bin (12)
in each los (152) containing the indices of pairs in a uniform
sample with same geometry as that los.
'''

from config import *

def main():

    # Load list of which los to loop over

    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    for p in todo_list:

        in_file = model_dir + 'uniform_' + p.ID + '.xyzw.dat'

        if not os.path.isfile(in_file):
            sys.stderr.write('Error: ' + in_file + ' does not exist.\n')
            continue

        # Count pairs in each bin

        for i in range(len(bins) - 1):

            param       = str(bins[i]) + ' ' + str(bins[i+1])

            output_file = model_dir + 'counts_' + p.ID + '.bin_' + str(i+1) +'.dat'

            cmd         = './uni_pair_count ' + in_file + ' ' + param + ' > ' + output_file

            os.system(cmd)

if __name__ == '__main__':
    main()