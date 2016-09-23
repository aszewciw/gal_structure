'''
Get chi2 when randoms have been run directly through pair counting.
'''

from config import *

def main():

    input_file = rawdata_dir + 'todo_list.dat'

    with open(input_file, 'rb') as data:
        todo_list = pickle.load(data)

    chi2 = 0

    for p in todo_list:

        mm_file = data_dir + 'MWM_dd_' + p.ID + '.dat'
        mm = np.genfromtxt(mm_file)

        err_file = errors_dir + 'frac_error_' + p.ID + '.dat'
        frac_err = np.genfromtxt(err_file)

        dd_file = dd_dir + 'dd_' + p.ID + '.dat'
        dd = np.genfromtxt(dd_file)

        for i in range(len(dd)):
            if frac_err[i]==0.0 or mm[i]==0.0:
                continue
            sig2 = (mm[i] * frac_err[i])**2
            chi2 += ((dd[i] - mm[i])**2)/sig2

    print(chi2)


if __name__ == '__main__':
    main()
