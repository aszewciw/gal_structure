from config import *
from scipy import linalg
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

'''
Describe what this does.
'''

#------------------------------------------------------------------------------#
def GIF_MOVIE(files, output_gif, delay=60, repeat=True, removef=False):
    """
    Given a list if 'files', it creates a gif file, and deletes temp files.

    Parameters
    ----------
    files: array_like
            List of abs. paths to temporary figures

    output_gif: str
            Absolute path to output gif file.
    """
    loop = -1 if repeat else 0
    os.system('convert -delay %d -loop %d %s %s' %( delay,loop," ".join(files), \
        output_gif) )

    if removef:
        for fname in files: os.remove(fname)
#------------------------------------------------------------------------------#
def plot_chi2_vs_z0thin(fignum, z0, chi2, truth_index, dict_key):

    MM = dict_key[0]
    R = dict_key[1]
    std = dict_key[2]

    # Set linestyle based on MM
    if MM == 't':
        MM = 'true'
        ls = '-'
    elif MM == 'e':
        MM = 'est'
        ls = '--'
    else:
        sys.stderr.write('Error! Invalid option for MM!\n')
        sys.exit()

    # Set marker properties based on correlation coefficient
    if R == 't':
        R = 'true'
        m = '*'
        ms = 12
    elif R == 'f':
        R = 'fid'
        m = 's'
        ms = 8
    elif R == 'n':
        R = 'none'
        m = 'p'
        ms = 9
    else:
        sys.stderr.write('Error! Invalid option for R!\n')
        sys.exit()

    # Set color based on standard deviation
    if std == 't':
        std = 'true'
        c = 'blue'
    elif std == 'e':
        std = 'est'
        c = 'red'
    elif std == 'f':
        std = 'fid'
        c = 'green'
    else:
        sys.stderr.write('Error! Invalid option for std!\n')
        sys.exit()

    la = r'$MM_{' + MM + '}, R_{' + R + '}, \sigma_{' + std + '}$'
    plt.figure(fignum)
    plt.plot(z0, chi2, marker=m, markersize=ms, color=c, linestyle=ls,
        label=la)
    plt.plot(z0[truth_index], chi2[truth_index], marker='o', color='cyan', markersize=13)

#------------------------------------------------------------------------------#

def calc_chi2(dict_key, di, dj, mm_ti, mm_tj, mm_ei, mm_ej, r_fid, r_true, std_ti, std_tj,
    frac_std_i, frac_std_j, std_fid_i, std_fid_j, i, j):

    # Check the dictionary key to understand how to calculate chi2
    if dict_key[0]=='t':
        mi = mm_ti
        mj = mm_tj
    elif dict_key[0]=='e':
        mi = mm_ei
        mj = mm_ej

    if dict_key[1]=='t':
        r = r_true
    elif dict_key[1]=='f':
        r = r_fid
    elif dict_key[1]=='n':
        if i==j:
            r=1
        else:
            r=0

    if dict_key[2]=='t':
        stdi = std_ti
        stdj = std_tj
    elif dict_key[2]=='f':
        stdi = std_fid_i
        stdj = std_fid_j
    elif dict_key[2]=='e':
        stdi = frac_std_i * mi
        stdj = frac_std_j * mj

    chi2 = (di - mi) * (dj - mj) * r / (stdi*stdj)

    return chi2



#------------------------------------------------------------------------------#

def main():

    ############################################################################
    ################################ CL Input ##################################
    ############################################################################

    '''
    Pass these arguments to the command line:
        N_lines -       number of lines in plot
        mock_num -      which mock realization (1-5000) we want to use for the "data"
        plt_string -    a string used to start the name of the output files

        remaining arguments - There should be N_lines of these. Each one is a 3
            letter string. Only particular strings are allowed. See below for my
            naming conventions and definitions.
    '''

    # Perform a few sanity checks
    args_array = np.array(sys.argv)
    N_args     = len(args_array)
    N_lines    = int(args_array[1])
    assert(N_lines != 0)
    assert(N_args == N_lines+4)
    mock_num   = args_array[2]
    plt_string = args_array[3]

    '''
    Define which possibilities I can plot.

    Naming conventions are as follows:
        1. First letter - Model pair counts (MM)
            t = true (mean of 5000 mocks)
            e = estimated (nonuniform)
        2. Second letter - correlation matrix:
            t = true (from 5000 mocks)
            f = fiducial
            n = none (i.e., independent chi2 calculation)
        3. Third letter - standard deviation:
            t = true (from 5000 mocks)
            e = estimated (nonuniform) - scaled with whichever MM we use
            f = fiducial
    '''

    # All combos I currently allow
    allowed_list = ['ttt', 'tte', 'ttf', 'tft', 'tfe', 'tff', 'tnt', 'tne', 'tnf',
                    'ett', 'ete', 'etf', 'eft', 'efe', 'eff', 'ent', 'ene', 'enf']

    # Exit if we're trying to plot more than we know how to plot
    if N_lines > len(allowed_list):
        sys.stderr.write('Error! Attempting to plot more possibilities than are allowed!\n')
        sys.exit()

    # Fill list of what we want to plot. Exit if we don't know what it means.
    line_list = []
    for i in range(N_lines):
        x = args_array[i+4]
        if not(x in allowed_list):
            sys.stderr.write('You passed an unallowed possibility!\n')
            sys.exit()
        line_list.append(x)

    ############################################################################
    ############################# Load/Initialize ##############################
    ############################################################################

    # Load list of pointing IDs
    todo_file = rawdata_dir + 'todo_list.ascii.dat'
    ID_list   = np.genfromtxt(todo_file, skip_header=1, usecols=[0], unpack=True,
                            dtype=str)
    N_los = len(ID_list)

    # Load bins centers and make column names for pandas
    bins_file   = rbins_dir + 'rbins.ascii.dat'
    bin_centers = np.genfromtxt(bins_file, skip_header=1, usecols=[2], unpack=True)
    N_bins      = len(bin_centers)

    bin_centers = np.round(bin_centers, 3)
    col_names = []
    for i in range(N_bins):
        name = str(bin_centers[i])
        col_names.append(name)
    col_names = np.asarray(col_names)

    # List of values of z0_thin (*1000) we have data for
    # Integers are used in filenames
    z0_thin = [183, 193, 203, 213, 223, 233, 243, 253, 263, 273, 283]

    # Dictionary of chi2 values for each thing we want to plot
    # Each line will have one chi2 value for each element of z0_thin
    CHI2 = {}
    for l in line_list:
        CHI2[l] = np.zeros(len(z0_thin))

    # Empty png list for plotting gif
    png_list = []

    ############################################################################
    ################################ Main Loop #################################
    ############################################################################

    # Loop over different values of "data"
    for k in range(len(z0_thin)):

        # Establish directories
        z = str(z0_thin[k])
        print('True z0_thin is 0.' + z)

        dd_dir = '../5000_mocks_' + z + '/errors_pairs/data/mock_' + mock_num + '/'

        # This directory is in a different place...
        if z=='233':
            dd_dir = '../../10000_mocks/errors_pairs/data/mock_' + mock_num + '/'

        # Calculate correlation matrix for each l.o.s.
        for ID in ID_list:

            # Load dd counts from whichever model we deemed "truth"
            # This is the "data"
            dd_file = dd_dir + 'mock_pairs_' + ID + '.dat'
            dd = np.genfromtxt(dd_file, unpack=True, usecols=[5])

            # Load fiducial mean and standard deviation
            mocks_fid_dir = '../../10000_mocks/errors_pairs/data/mean_var_std/'
            mock_fid_file = mocks_fid_dir + 'stats_' + ID + '.dat'
            mm_mean_fid, std_fid = np.genfromtxt(mock_fid_file, unpack=True, usecols=[0,2])

            # Get fractional std from fiducial for error scaling
            frac_std = std_fid / mm_mean_fid

            # Load correlation matrix of fiducial and invert
            corr_filename = out_dir + 'z0thin_233_corr_mat_' + ID + '.dat'
            corr_fid = np.genfromtxt(corr_filename)
            inv_corr_fid = linalg.inv(corr_fid)

            for f in range(len(z0_thin)):

                Z = str(z0_thin[f])

                # Load real mean and std
                mocks_dir = '../5000_mocks_' + Z + '/errors_pairs/data/mean_var_std/'
                if Z == '233':
                    mocks_dir = '../../10000_mocks/errors_pairs/data/mean_var_std/'
                mock_file = mocks_dir + 'stats_' + ID + '.dat'
                mm_mean, std = np.genfromtxt(mock_file, unpack=True, usecols=[0,2])

                # Load real correlation matrix
                corr_filename = out_dir + 'z0thin_' + str(z) + '_corr_mat_' + ID + '.dat'
                corr = np.genfromtxt(corr_filename)
                inv_corr = linalg.inv(corr)

                # Load nonuniform estimated mean
                if Z == '233': Z = 'fid'
                pairs_dir = '../pair_count_' + Z + '/data/'
                nonuni_file = pairs_dir + 'mm_nonuni_' + ID + '.dat'
                mm_nonuni = np.genfromtxt(nonuni_file)

                # Calculate chi2 using a number of different methods
                for i in range(N_bins):

                    for j in range(N_bins):

                        # Data points from this mock
                        data_i = dd[i]
                        data_j = dd[j]

                        # Means from 1000 mocks
                        model_true_i = mm_mean[i]
                        model_true_j = mm_mean[j]

                        # Weighted random approximation to mean
                        model_est_i = mm_nonuni[i]
                        model_est_j = mm_nonuni[j]

                        # Inverse correlation matrix element
                        r_ij_fid  = inv_corr_fid[i,j]
                        r_ij_true = inv_corr[i,j]

                        # Actual standard deviations from 1000 mocks
                        std_true_i = std[i]
                        std_true_j = std[j]

                        # Fractional standard deviations
                        frac_std_i = frac_std[i]
                        frac_std_j = frac_std[j]

                        # Fiducial standard deviation
                        std_fid_i = std_fid[i]
                        std_fid_j = std_fid[j]


                        for l in line_list:
                            chi2_temp = calc_chi2(
                                dict_key=l, di=data_i, dj=data_j,
                                mm_ti=model_true_i, mm_tj=model_true_j,
                                mm_ei=model_est_i, mm_ej=model_est_j,
                                r_fid=r_ij_fid, r_true=r_ij_true,
                                std_ti=std_true_i, std_tj=std_true_j,
                                frac_std_i=frac_std_i, frac_std_j=frac_std_j,
                                std_fid_i=std_fid_i, std_fid_j=std_fid_j,
                                i=i, j=j
                                )

                            CHI2[l][f] += chi2_temp


        z0 = np.asarray(z0_thin)
        z0 = z0/1000.0

        plt.clf()
        plt.figure(1)
        plt.xlabel(r'$z_{0,thin}$', fontsize=18)
        plt.ylabel(r'$\chi^2$', fontsize=18)

        for l in line_list:
            plot_chi2_vs_z0thin(fignum=1, z0=z0, chi2=CHI2[l], truth_index=k,
                dict_key=l)

        plt.legend(numpoints=1, loc='upper left', fontsize=8)
        plt.tight_layout()
        fig_name = plots_dir + 'chi2_z' + z + '_m' + mock_num + '.png'
        plt.savefig(fig_name)
        png_list.append(fig_name)

    chi2_gif = plots_dir + plt_string + '_m' + mock_num + '.gif'

    GIF_MOVIE(png_list, chi2_gif, delay=120, removef=True)

if __name__ == '__main__':
    main()