import matplotlib.pyplot as plt
import numpy as np
from config import *

#find parameters for Qingqing's minimum chi2 value

def main():
    elements_needed = int(3)

    args_array = np.array(sys.argv)
    N_args = len(args_array)
    assert(N_args == elements_needed)
    in_file = args_array[1]
    out_file = args_array[2]

    # qiqi_file = qiqi_dir + 'mcmc_result.dat'

    rthin, zthin, rthick, zthick, a, chi2 = np.genfromtxt(qiqi_file,
        unpack=True, usecols=[1, 2, 3, 4, 5, 6])

    min_index = np.argmin(chi2)

    print('Best chi2 is:   ', chi2[min_index])
    print('Best rthin is:  ', rthin[min_index])
    print('Best zthin is:  ', zthin[min_index])
    print('Best rthick is: ', rthick[min_index])
    print('Best zthick is: ', zthick[min_index])
    print('Best a is:      ', a[min_index])

    result_file = './data/' + out_file
    result_data = np.array([chi2[min_index], rthin[min_index], zthin[min_index],
        rthick[min_index], zthick[min_index], a[min_index]])
    np.savetxt(result_file, result_data)

if __name__ == '__main__':
    main()