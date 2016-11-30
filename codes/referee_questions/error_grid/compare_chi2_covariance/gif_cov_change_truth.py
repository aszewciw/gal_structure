from config import *
from scipy import linalg
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# rawdata_dir  = '../../data/'
# data_dir     = '../data/'
# mock_dir     = '../../prepare_mock/data/'
# uni_dir      = '../../prepare_randoms/data/'
# errors_dir   = data_dir + 'errors/'
# mcmc_out_dir = data_dir + 'mcmc_output/'
# mock_dd_dir  = data_dir + 'mock_dd/'
# pairs_dir    = data_dir + 'model_pairs/'
# zrw_dir      = data_dir + 'model_positions/'
# rbins_dir    = data_dir + 'rbins/'
# # sigma_dir    = '../../1000_mocks_cut/errors_pairs/data/mean_var_std/'
# # counts_dir   = '../../1000_mocks_cut/errors_pairs/data/'
# sigma_dir    = '../../10000_mocks/errors_pairs/data/mean_var_std/'
# counts_dir   = '../../10000_mocks/errors_pairs/data/'

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

def main():

    elements_needed = int(2)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args == elements_needed)
    mock_num   = args_array[1]

    # Load list of pointing IDs
    todo_file = rawdata_dir + 'todo_list.ascii.dat'
    ID_list   = np.genfromtxt(todo_file, skip_header=1, usecols=[0], unpack=True,
                            dtype=str)
    N_los = len(ID_list)

    # Load bins centers
    bins_file   = rbins_dir + 'rbins.ascii.dat'
    bin_centers = np.genfromtxt(bins_file, skip_header=1, usecols=[2], unpack=True)
    N_bins      = len(bin_centers)

    # Round bin centers to three decimal places
    bin_centers = np.round(bin_centers, 3)

    # Make array of column names for pandas Dataframe
    col_names = []

    for i in range(N_bins):
        name = str(bin_centers[i])
        col_names.append(name)

    # Recast as array
    col_names = np.asarray(col_names)

    z0_thin = [183, 193, 203, 213, 223, 233, 243, 253, 263, 273]

    png_list = []

    for k in range(len(z0_thin)):

        if k>0: continue

        z = str(z0_thin[k])

        dd_dir = '../5000_mocks_' + z + '/errors_pairs/data/mock_' + mock_num + '/'

        if z=='233':
            dd_dir = '../../10000_mocks/errors_pairs/data/mock_' + mock_num + '/'

        chi2_true = np.zeros(len(z0_thin))
        # chi2_uni  = np.zeros(len(z0_thin))
        chi2_nonuni = np.zeros(len(z0_thin))

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
                        r_ij_fid = inv_corr_fid[i,j]
                        r_ij = inv_corr[i,j]

                        # Actual standard deviations from 1000 mocks
                        std_true_i = std[i]
                        std_true_j = std[j]

                        # Estimated standard deviations from 1000 mocks
                        std_est_i = frac_std[i]*model_est_i
                        std_est_j = frac_std[j]*model_est_j

                        # uniform estimated
                        chi2_true[f] += ( (data_i-model_true_i) * (data_j-model_true_j) * r_ij
                            / (std_true_i*std_true_j) )

                        # nonuniform estimated
                        chi2_nonuni[f] += ( (data_i-model_true_i) * (data_j-model_true_j) * r_ij_fid
                            / (std_est_i*std_est_j) )

                        # # Use weighted random mm and true std
                        # chi2_et_cov += ( (data_i-model_est_i) * (data_j-model_est_j) * r_ij
                        #     / (std_true_i*std_true_j) )

                        # # Use weighted random mm and estimated std
                        # chi2_ee_cov += ( (data_i-model_est_i) * (data_j-model_est_j) * r_ij
                        #     / (std_est_i*std_est_j) )

        z0 = np.asarray(z0_thin)
        z0 = z0/1000.0

        plt.clf()
        plt.figure(1)
        plt.xlabel(r'$z_{0,thin}$', fontsize=18)
        plt.ylabel(r'$\chi^2$', fontsize=18)
        # plt.plot(z0, chi2_uni, marker='*', color='blue', label='uniform')
        # plt.plot(z0[k], chi2_uni[k], marker='o', color='cyan', markersize=15)
        plt.plot(z0, chi2_nonuni, marker='^', color='green', label='nonuniform')
        plt.plot(z0[k], chi2_nonuni[k], marker='o', color='cyan', markersize=15)
        plt.plot(z0, chi2_true, marker='s', color='red', label='true')
        plt.plot(z0[k], chi2_true[k], marker='o', color='cyan', markersize=15)
        plt.legend(numpoints=1, loc='upper left')
        plt.tight_layout()
        # plt.axis([z0[0]-0.01,z0[-1]+0.01,1500,3000])
        fig_name = plots_dir + 'chi2_z' + z + '_m' + mock_num + '.png'
        plt.savefig(fig_name)
        # png_list.append(fig_name)

    # chi2_gif = plots_dir + 'chi2_m' + mock_num + '.gif'

    # GIF_MOVIE(png_list, chi2_gif, delay=120, removef=True)


        # print('\nResults of chi-squared measurements for diffferent instances:\n')
        # print('Using true mean and true stdev:')
        # print('     Without covariance: {}, With covariance: {}'.format(chi2_tt, chi2_tt_cov))
        # print('Using true mean and estimated stdev:')
        # print('     Without covariance: {}, With covariance: {}'.format(chi2_te, chi2_te_cov))
        # print('Using estimated mean and true stdev:')
        # print('     Without covariance: {}, With covariance: {}'.format(chi2_et, chi2_et_cov))
        # print('Using estimate mean and estimated stdev:')
        # print('     Without covariance: {}, With covariance: {}'.format(chi2_ee, chi2_ee_cov))
        # print('\nThere were {}/{} values of dd=0 for this mock.'.format(zero_counts,all_counts))

if __name__ == '__main__':
    main()