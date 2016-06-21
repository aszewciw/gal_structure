from config import *

def main():

    # load the todo pointing list
    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    # load the bin list
    bins_file = rbins_dir + 'rbins.dat'
    rlower, rupper = np.genfromtxt(bins_file, skip_header=1, unpack=True,
        usecols=[0,1])

    Nbins = len(rlower)

    for p in todo_list:

        # a progress indicator
        if todo_list.index(p) % 10 == 0:
            sys.stderr.write('On pointing #{} of {} ..\n'
                             .format(todo_list.index(p), len(todo_list)))

        random_file = uni_dir + 'uniform_' + p.ID + '.ascii.dat'
        distance, Z, R = np.genfromtxt( random_file, skip_header=1,
            unpack=True, usecols=[2,5,6] )

        for i in range(Nbins):

            r1 = rlower[i]
            r2 = rupper[i]
            indices = np.where((distance>r1)&(distance<=r2))[0]

            Z_bin = Z[indices]
            R_bin = R[indices]

            N_stars = len(Z_bin)

            output_file = ( zr_dir + 'uniform_ZR_' + p.ID + '_bin_'
                + str(i) + '.dat' )

            with open(output_file, 'w') as f:
                f.write(str(N_stars))
                f.write('\n')
                for j in range(N_stars):
                    f.write('{}\t{}\n'.format(Z_bin[j], R_bin[j]))


if __name__ == '__main__':
     main()
