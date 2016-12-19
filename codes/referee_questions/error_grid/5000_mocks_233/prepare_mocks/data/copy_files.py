import os, sys

def main():

    file_dir = '/fs1/szewciw/gal_structure/codes/referee_questions/10000_mocks/prepare_mocks/data'

    i = 1

    while i<5001:

        print('Copying folder ' + str(i))
        folder = file_dir + 'mock_' + '/' + str(i)
        cmd = 'cp -rp ' + folder + ' ./'

        os.system(cmd)

        i = i+1

if __name__ == '__main__':
    main()