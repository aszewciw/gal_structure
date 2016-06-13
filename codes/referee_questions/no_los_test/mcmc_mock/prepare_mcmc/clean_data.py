from config import *

def main():

    # Repack uniform error files
    uni_jk_file = jk_dir + 'uniform_jk_error.dat'
    uni_jk_err  = np.genfromtxt(uni_jk_file, unpack=True, usecols=[7])
    outfile     = errors_dir + 'uniform_frac_error.dat'
    np.savetxt(outfile, uni_jk_err)

    # Repack mock error files
    dat_jk_file = jk_dir + 'mock_jk_error.dat'
    dat_jk_err  = np.genfromtxt(dat_jk_file, unpack=True, usecols=[7])
    outfile     = errors_dir + 'mock_frac_error.dat'
    np.savetxt(outfile, dat_jk_err)

if __name__ == '__main__':
    main()
