'''
More dumb stuff: make todo have only pointing IDs
'''
import numpy as np

def main():

    todo_file = '../data/raw/todo_list.ascii.dat'
    ID        = np.genfromtxt(todo_file, unpack=True, usecols=[0], dtype=str)
    outfile   = '../data/raw/pointing_ID.dat'

    with open(outfile, 'w') as f:
        for i in range(len(ID)):
            f.write("{}\n".format(ID[i]))

if __name__ == '__main__':
    main()