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
    mod_true     = args_array[1]

    # Load list of pointing IDs
    todo_file = rawdata_dir + 'todo_list.ascii.dat'
    ID_list   = np.genfromtxt(todo_file, skip_header=1, usecols=[0], unpack=True,
                            dtype=str)
    N_los = len(ID_list)

    # Load bins centers
    bins_file   = pairs_dir + 'rbins.ascii.dat'
    bin_centers = np.genfromtxt(bins_file, skip_header=1, usecols=[2], unpack=True)
    N_bins      = len(bin_centers)

    # Round bin centers to three decimal places
    bin_centers = np.round(bin_centers, 3)

    # Create list of png's for use in making gif
    png_list = []


    chi2_A_tt      = 0.0
    chi2_A_et      = 0.0
    chi2_A_te_frac = 0.0
    chi2_A_ee_frac = 0.0

    chi2_B_tt      = 0.0
    chi2_B_et      = 0.0
    chi2_B_te_frac = 0.0
    chi2_B_ee_frac = 0.0

    chi2_C_tt      = 0.0
    chi2_C_et      = 0.0
    chi2_C_te_frac = 0.0
    chi2_C_ee_frac = 0.0


    # Calculate correlation matrix for each l.o.s.
    for ID in ID_list:

        # Load stats for model A (fiducial)
        mock_file = modA_err_dir + 'stats_' + ID + '.dat'
        mm_mean_A, std_A = np.genfromtxt(mock_file, unpack=True, usecols=[0,2])

        # Load weighted nonuniform counts for model A
        w_file = pairs_dir + 'mm_A_' + ID + '.dat'
        mm_A = np.genfromtxt(w_file)


        # Load stats for model B
        mock_file = modB_err_dir + 'stats_' + ID + '.dat'
        mm_mean_B, std_B = np.genfromtxt(mock_file, unpack=True, usecols=[0,2])

        # Load weighted nonuniform counts for model B
        w_file = pairs_dir + 'mm_B_' + ID + '.dat'
        mm_B = np.genfromtxt(w_file)


        # Load stats for model C
        mock_file = modC_err_dir + 'stats_' + ID + '.dat'
        mm_mean_C, std_C = np.genfromtxt(mock_file, unpack=True, usecols=[0,2])

        # Load weighted nonuniform counts for model C
        w_file = pairs_dir + 'mm_C_' + ID + '.dat'
        mm_C = np.genfromtxt(w_file)


        # Load dd counts from whichever model we deemed "truth"
        dd_file = dd_dir + 'mod_' + mod_true + '_mm_' + ID + '.dat'
        dd = np.genfromtxt(dd_file)

        # Calculate fractional std: std/mean for fiducial
        frac_std_A = std_A / mm_mean_A


        for i in range(len(dd)):

            if dd[i]==0.0: continue
            DD = dd[i]

            # True true
            chi2_A_tt += ( (mm_mean_A[i] - DD) / std_A[i] )**2
            chi2_B_tt += ( (mm_mean_B[i] - DD) / std_B[i] )**2
            chi2_C_tt += ( (mm_mean_C[i] - DD) / std_C[i] )**2

            # est true
            chi2_A_et += ( (mm_A[i] - DD) / std_A[i] )**2
            chi2_B_et += ( (mm_B[i] - DD) / std_B[i] )**2
            chi2_C_et += ( (mm_C[i] - DD) / std_C[i] )**2

            # Using just fiducial std
            # True est_fid
            # chi2_A_te_fid += ( (mm_mean_A[i] - DD) / std_A[i] )**2
            # chi2_B_te_fid += ( (mm_mean_B[i] - DD) / std_A[i] )**2
            # chi2_C_te_fid += ( (mm_mean_C[i] - DD) / std_A[i] )**2

            # # est est_fid
            # chi2_A_ee_fid += ( (mm_A[i] - DD) / std_A[i] )**2
            # chi2_B_ee_fid += ( (mm_B[i] - DD) / std_A[i] )**2
            # chi2_C_ee_fid += ( (mm_C[i] - DD) / std_A[i] )**2

            # Using fiducial fractional errors, weighted by estimated MM
            STD_A = frac_std_A[i] * mm_A[i]
            STD_B = frac_std_A[i] * mm_B[i]
            STD_C = frac_std_A[i] * mm_C[i]

            # true est_frac
            chi2_A_te_frac += ( (mm_mean_A[i] - DD) / STD_A )**2
            chi2_B_te_frac += ( (mm_mean_B[i] - DD) / STD_B )**2
            chi2_C_te_frac += ( (mm_mean_C[i] - DD) / STD_C )**2

            # est est_frac
            chi2_A_ee_frac += ( (mm_A[i] - DD) / std_A )**2
            chi2_B_ee_frac += ( (mm_B[i] - DD) / std_B )**2
            chi2_C_ee_frac += ( (mm_C[i] - DD) / std_C )**2


    tt      = np.array([chi2_A_tt, chi2_B_tt, chi2_C_tt])
    et      = np.array([chi2_A_et, chi2_B_et, chi2_C_et])
    # te_fid  = np.array([chi2_A_te_fid, chi2_B_te_fid, chi2_C_te_fid])
    # ee_fid  = np.array([chi2_A_ee_fid, chi2_B_ee_fid, chi2_C_ee_fid])
    te_frac = np.array([chi2_A_te_frac, chi2_B_te_frac, chi2_C_te_frac])
    ee_frac = np.array([chi2_A_ee_frac, chi2_B_ee_frac, chi2_C_ee_frac])

    models = np.array([1,2,3])

    plt.clf()
    plt.figure(1)
    plt.axis([0.5, 3.5, 1800, 3600])
    plt.xlabel('Model type (1 is fiducial)')
    plt.ylabel(r'$\chi^2$')
    plt.plot(models, tt, marker='*', label=r'$MM_{true}, \sigma_{true}$')
    plt.plot(models, et, marker='^', label=r'$MM_{est}, \sigma_{true}$')
    # plt.plot(models, te_fid, marker='s', label=r'$MM_{true}, \sigma_{fid}$')
    # plt.plot(models, ee_fid, marker='o', label=r'$MM_{est}, \sigma_{fid}$')
    plt.plot(models, te_frac, marker='h', label=r'$MM_{true}, \sigma_{est}$')
    plt.plot(models, ee_frac, marker='p', label=r'$MM_{est}, \sigma_{est}$')
    plt.legend(numpoints=1, loc='upper left')

    fig_name = plots_dir + 'chi2_fidA_true_' + mod_true + '.png'

    plt.savefig(fig_name)


if __name__ == '__main__':
    main()