from config import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#------------------------------------------------------------------------------#
'''
Produce a correlation matrix plot for each SEGUE l.o.s. using 1000 mocks.
Make a gif from the files.
'''

#------------------------------------------------------------------------------#

def main():

    # CL Input
    # star_factor = N_random / N_data in each l.o.s.
    elements_needed = int(2)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args == elements_needed)
    N     = int(args_array[1])

    # Load list of pointing IDs
    todo_file = rawdata_dir + 'todo_list.ascii.dat'
    ID_list   = np.genfromtxt(todo_file, skip_header=1, usecols=[0], unpack=True,
                            dtype=str)
    N_los = len(ID_list)

    # Load bins centers
    bins_file   = pairs0_dir + 'rbins.ascii.dat'
    bin_centers = np.genfromtxt(bins_file, skip_header=1, usecols=[2], unpack=True)
    N_bins      = len(bin_centers)

    # Round bin centers to three decimal places
    bin_centers = np.round(bin_centers, 3)

    # chi2_0_tt      = 0.0
    # chi2_0_et      = 0.0
    # chi2_0_te_frac = 0.0
    # chi2_0_ee_frac = 0.0
    # chi2_0_te_fid  = 0.0
    # chi2_0_ee_fid  = 0.0

    # chi2_1_tt      = 0.0
    # chi2_1_et      = 0.0
    # chi2_1_te_frac = 0.0
    # chi2_1_ee_frac = 0.0
    # chi2_1_te_fid  = 0.0
    # chi2_1_ee_fid  = 0.0

    # chi2_2_tt      = 0.0
    # chi2_2_et      = 0.0
    # chi2_2_te_frac = 0.0
    # chi2_2_ee_frac = 0.0
    # chi2_2_te_fid  = 0.0
    # chi2_2_ee_fid  = 0.0

    chi2_0_true = np.zeros(N_bins)
    chi2_0_est  = np.zeros(N_bins)

    chi2_1_true = np.zeros(N_bins)
    chi2_1_est  = np.zeros(N_bins)

    chi2_2_true = np.zeros(N_bins)
    chi2_2_est  = np.zeros(N_bins)

    # Calculate correlation matrix for each l.o.s.
    for ID in ID_list:

        # Load stats for model 0 (fiducial)
        mock_file = mod0_dir + 'stats_' + ID + '.dat'
        mm_mean_0, std_0 = np.genfromtxt(mock_file, unpack=True, usecols=[0,2])

        # Load weighted random counts for model 0
        w_file = pairs0_dir + 'mm_' + str(N) + '_' + ID + '.dat'
        mm_0 = np.genfromtxt(w_file)

        # Load stats for model 1
        mock_file = mod1_dir + 'stats_' + ID + '.dat'
        mm_mean_1, std_1 = np.genfromtxt(mock_file, unpack=True, usecols=[0,2])

        # Load weighted random counts for model 1
        w_file = pairs1_dir + 'mm_' + str(N) + '_' + ID + '.dat'
        mm_1 = np.genfromtxt(w_file)

        # Load stats for model 2
        mock_file = mod2_dir + 'stats_' + ID + '.dat'
        mm_mean_2, std_2 = np.genfromtxt(mock_file, unpack=True, usecols=[0,2])

        # Load weighted random counts for model 2
        w_file = pairs2_dir + 'mm_' + str(N) + '_' + ID + '.dat'
        mm_2 = np.genfromtxt(w_file)

        # Load dd counts from one mock
        dd_file = dd_dir + 'dd_' + ID + '.dat'
        dd = np.genfromtxt(dd_file)

        # Calculate fractional std: std/mean for fiducial
        frac_std_0 = std_0 / mm_mean_0

        for i in range(N_bins):

            if dd[i]==0.0: continue
            DD = dd[i]

            # Add to true chi2 values
            chi2_0_true[i] += ( (mm_mean_0[i] - DD) / std_0[i] )**2
            chi2_1_true[i] += ( (mm_mean_1[i] - DD) / std_1[i] )**2
            chi2_2_true[i] += ( (mm_mean_2[i] - DD) / std_2[i] )**2

            # Add to estimated chi2 values
            # Use fiducial fractional errors, weighted by estimated MM
            STD_0 = frac_std_0[i] * mm_0[i]
            STD_1 = frac_std_0[i] * mm_1[i]
            STD_2 = frac_std_0[i] * mm_2[i]
            chi2_0_est[i] += ( (mm_0[i] - DD) / STD_0 )**2
            chi2_1_est[i] += ( (mm_1[i] - DD) / STD_1 )**2
            chi2_2_est[i] += ( (mm_2[i] - DD) / STD_2 )**2


            # # True true
            # chi2_0_tt += ( (mm_mean_0[i] - DD) / std_0[i] )**2
            # chi2_1_tt += ( (mm_mean_1[i] - DD) / std_1[i] )**2
            # chi2_2_tt += ( (mm_mean_2[i] - DD) / std_2[i] )**2

            # # est true
            # chi2_0_et += ( (mm_0[i] - DD) / std_0[i] )**2
            # chi2_1_et += ( (mm_1[i] - DD) / std_1[i] )**2
            # chi2_2_et += ( (mm_2[i] - DD) / std_2[i] )**2

            # # Using just fiducial std
            # # True est_fid
            # chi2_0_te_fid += ( (mm_mean_0[i] - DD) / std_0[i] )**2
            # chi2_1_te_fid += ( (mm_mean_1[i] - DD) / std_0[i] )**2
            # chi2_2_te_fid += ( (mm_mean_2[i] - DD) / std_0[i] )**2

            # # est est_fid
            # chi2_0_ee_fid += ( (mm_0[i] - DD) / std_0[i] )**2
            # chi2_1_ee_fid += ( (mm_1[i] - DD) / std_0[i] )**2
            # chi2_2_ee_fid += ( (mm_2[i] - DD) / std_0[i] )**2

            # # Using fiducial fractional errors, weighted by estimated MM
            # STD_0 = frac_std_0[i] * mm_0[i]
            # STD_1 = frac_std_0[i] * mm_1[i]
            # STD_2 = frac_std_0[i] * mm_2[i]

            # # true est_frac
            # chi2_0_te_frac += ( (mm_mean_0[i] - DD) / STD_0 )**2
            # chi2_1_te_frac += ( (mm_mean_1[i] - DD) / STD_1 )**2
            # chi2_2_te_frac += ( (mm_mean_2[i] - DD) / STD_2 )**2

            # # est est_frac
            # chi2_0_ee_frac += ( (mm_0[i] - DD) / STD_0 )**2
            # chi2_1_ee_frac += ( (mm_1[i] - DD) / STD_1 )**2
            # chi2_2_ee_frac += ( (mm_2[i] - DD) / STD_2 )**2


    # tt      = np.array([chi2_0_tt, chi2_1_tt, chi2_2_tt])
    # et      = np.array([chi2_0_et, chi2_1_et, chi2_2_et])
    # te_fid  = np.array([chi2_0_te_fid, chi2_1_te_fid, chi2_2_te_fid])
    # ee_fid  = np.array([chi2_0_ee_fid, chi2_1_ee_fid, chi2_2_ee_fid])
    # te_frac = np.array([chi2_0_te_frac, chi2_1_te_frac, chi2_2_te_frac])
    # ee_frac = np.array([chi2_0_ee_frac, chi2_1_ee_frac, chi2_2_ee_frac])

    # models = np.array([1,2,3])

    plt.clf()
    # plt.axis([0.5, 3.5, 1800, 3600])
    plt.xlabel('Bin Centers (kpc)')
    plt.ylabel(r'$\chi^2$')

    plt.semilogx(bin_centers, chi2_0_true, marker='*', label='Mod. 0, True')
    plt.semilogx(bin_centers, chi2_0_est, marker='^', label='Mod. 0, Est')
    plt.semilogx(bin_centers, chi2_1_true, marker='s', label='Mod. 1, True')
    plt.semilogx(bin_centers, chi2_1_est, marker='o', label='Mod. 1, Est.')
    plt.semilogx(bin_centers, chi2_2_true, marker='h', label='Mod. 2, True')
    plt.semilogx(bin_centers, chi2_2_est, marker='p', label='Mod. 2, Est.')

    # plt.plot(models, tt, marker='*', label=r'$MM_{true}, \sigma_{true}$')
    # plt.plot(models, et, marker='^', label=r'$MM_{est}, \sigma_{true}$')
    # plt.plot(models, te_fid, marker='s', label=r'$MM_{true}, \sigma_{fid}$')
    # plt.plot(models, ee_fid, marker='o', label=r'$MM_{est}, \sigma_{fid}$')
    # plt.plot(models, te_frac, marker='h', label=r'$MM_{true}, \sigma_{est}$')
    # plt.plot(models, ee_frac, marker='p', label=r'$MM_{est}, \sigma_{est}$')
    plt.legend(numpoints=1, loc='upper left')

    fig_name = plots_dir + 'chi2_bin_' + str(N) + '.png'

    plt.savefig(fig_name)


if __name__ == '__main__':
    main()