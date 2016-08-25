from config import *
import matplotlib.pyplot as plt

def main():

    elements_needed = int(2)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args   == elements_needed)
    infile         = args_array[1]
    infile         = out_dir + infile

    mm_corr, mm_mcmc, los_num, bin_num = np.genfromtxt(infile, unpack = True)

    index = np.arange(len(mm_corr))
    diff = mm_corr - mm_mcmc
    plt.plot(index, diff)
    plt.show()

if __name__ == '__main__':
    main()