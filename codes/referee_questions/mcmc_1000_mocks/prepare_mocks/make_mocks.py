import numpy as np
import os, sys

def main():

    elements_needed = int(3)

    args_array = np.array(sys.argv)
    N_args = len(args_array)
    assert(N_args == elements_needed)
    N_stars = args_array[1]
    N_mocks = int(args_array[2])

    for i in range(N_mocks):

        mock_dir = '../data/mock_' + str(i+1) +'/'

        cmd = 'time ./bin/make_galaxy ' + N_stars + ' ' + str(i+1)
        os.system(cmd)

        cmd2 = 'python clean_mocks.py ' + str(i+1)
        os.system(cmd2)

        cmd3 = 'rm ' + mock_dir + 'temp*'
        os.system(cmd3)

if __name__ == '__main__':
    main()