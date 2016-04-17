'''
More dumb stuff: make todo have only pointing IDs
'''
import numpy as np

def main():

    todo_file = '../data/raw/todo_list.ascii.dat'
    ID        = np.genfromtxt(todo_file, unpack=True, usecols=[0], dtype=int)
    outfile   = '../data/raw/pointing_ID.dat'
    np.savetxt(outfile, ID)

if __name__ == '__main__':
    main()