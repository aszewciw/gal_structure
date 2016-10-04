'''
Loops over all SEGUE los and produces a file for each
mock containing the normalized dd counts.
'''

# from config import *
rawdata_dir = '../../data/'
rbins_dir = '../data/rbins/'
mwm_dir = './data/'

def main():

    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    bins_file = rbins_dir + 'rbins.ascii.dat'
    if not os.path.isfile(bins_file):
        sys.stderr.write('Error: ' + bins_file + ' does not exist.\n')

    for p in todo_list:

        in_file = mwm_dir + 'MWM_' + p.ID + '.xyzw.dat'

        if not os.path.isfile(in_file):
            sys.stderr.write('Error: ' + in_file + ' does not exist.\n')
            continue

        output_file = mwm_dir + 'mm_' + p.ID + '.dat'

        cmd = ( './pair_pair_count ' + in_file + ' ' + bins_file
            + ' > ' + output_file )
        os.system(cmd)

if __name__ == '__main__':
    main()