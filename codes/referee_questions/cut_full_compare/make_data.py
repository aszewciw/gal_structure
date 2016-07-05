import numpy as np
import matplotlib.pyplot as plt
import math

# folders containing counts and standard deviations
cut_dir        = '../mcmc_1000_mocks_cut/data/'
cut_dd_dir     = cut_dir + 'mock_dd/'
cut_sigma_dir  = cut_dir + 'errors/'
full_dir       = '../mcmc_1000_mocks_full/data/'
full_dd_dir    = full_dir + 'mock_dd/'
full_sigma_dir = full_dir + 'errors/'
pointing_dir   = '../data/'
bins_dir       = cut_dir + 'rbins/'

def propagate_error(f, g, f_sigma, g_sigma):

    '''
    Propagate error of f/g.

    Return f/g and error in f/g.
    '''

    N = len(f)

    h       = np.zeros(N)
    h_sigma = np.zeros(N)

    for i in range(N):

        if (g[i] == 0.0) or (f[i] == 0.0):
            continue

        h[i] = f[i] / g[i]

    for i in range(N):

        if h[i] == 0.0:
            continue

        term1 = f_sigma[i]**2 / f[i]**2
        term2 = g_sigma[i]**2 / g[i]**2
        h_sigma[i] = math.sqrt( (term1 + term2) * h[i]**2 )

    return h, h_sigma


def main():

    # First load pointing IDs
    todo_file = pointing_dir + 'todo_list.ascii.dat'
    ID_list   = np.genfromtxt(todo_file, skip_header=1, usecols=[0], unpack=True,
                dtype=int)
    N_los     = len(ID_list)

    # Read in number of bins
    bins_file = bins_dir + 'rbins.ascii.dat'
    bins      = np.genfromtxt(bins_file, skip_header=1)
    N_bins    = len(bins)

    # empty arrays (N_los by N_bins) to be filled with file data
    cut_over_full = np.zeros((N_los, N_bins))   # dd_cut / dd_full
    weight1       = np.zeros((N_los, N_bins))   # 1 / sigma weight
    weight2       = np.zeros((N_los, N_bins))   # 1 / sigma^2 weight

    # Get data for each pointing
    for j in range(N_los):

        # string for file read in
        ID = str(ID_list[j])

        # Normalized pair counts of cut sample
        cut_dd_file = cut_dd_dir + 'dd_' + ID + '.dat'
        cut_dd      = np.genfromtxt(cut_dd_file)

        # Sigma for cut sample
        cut_sigma_file = cut_sigma_dir + 'mock_' + ID + '_frac_error.dat'
        cut_sigma      = np.genfromtxt(cut_sigma_file)

        # Normalized pair counts of full sample
        full_dd_file = full_dd_dir + 'dd_' + ID + '.dat'
        full_dd      = np.genfromtxt(full_dd_file)

        # Sigma for full sample
        full_sigma_file = full_sigma_dir + 'mock_' + ID + '_frac_error.dat'
        full_sigma      = np.genfromtxt(full_sigma_file)

        # Get dd_cut / dd_full
        fraction, sigma = propagate_error( cut_dd, full_dd, cut_sigma,
                            full_sigma )

        # Initialize and calculate weights for weighted mean
        w1 = np.zeros(len(sigma))
        w2 = np.zeros(len(sigma))

        for i in range(len(sigma)):

            if sigma[i]==0.0:
                continue

            w1[i] = 1/sigma[i]
            w2[i] = w1[i]**2

        # Assign to main array
        cut_over_full[j,:] = fraction
        weight1[j,:]       = w1
        weight2[j,:]       = w2

    # Find two different weighted means

    numerator = weight1 * cut_over_full
    w_mean_1  = np.sum(numerator, axis=0) / np.sum(weight1, axis=0)

    numerator = weight2 * cut_over_full
    w_mean_2  = np.sum(numerator, axis=0) / np.sum(weight2, axis=0)

    # variance in mean is 1 / sum(1/var_i)
    var_mean  = 1 / np.sum(weight2, axis=0)
    std_mean  = np.sqrt(var_mean)

    # Output files to current directory

    filename = 'w_mean_1.dat'
    np.savetxt(filename, w_mean_1)

    filename = 'w_mean_2.dat'
    np.savetxt(filename, w_mean_2)

    filename = 'std_mean.dat'
    np.savetxt(filename, std_mean)




if __name__ == '__main__':
    main()