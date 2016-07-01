import numpy as np
import os, sys

def main():

    false_total = 200

    length=[]

    for i in range(false_total):

        ID = str(i)

        file = 'mock_' + ID + '.xyz.dat'

        if not os.path.isfile(file):
            continue

        array = np.genfromtxt(file, skip_header=1)
        N_stars = len(array)
        length.append(N_stars)

    print(min(length), max(length))



if __name__ == '__main__':
    main()