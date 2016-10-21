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

    # Create list of png's for use in making gif
    png_list = []

    org_patch = mpatches.Patch(color='#CC4F1B', label=r'$MM_{mean}$')
    black_patch = mpatches.Patch(color='black', label=r'$MM_{10}$')
    green_patch = mpatches.Patch(color='green', label=r'$MM_{50}$')
    blue_patch = mpatches.Patch(color='blue', label=r'$MM_{100}$')
    red_patch = mpatches.Patch(color='red', label=r'$MM_{1000}$')

    chi2_0_tt      = 0.0
    chi2_0_et      = 0.0
    chi2_0_te_frac = 0.0
    chi2_0_ee_frac = 0.0
    chi2_0_te_fid  = 0.0
    chi2_0_ee_fid  = 0.0

    chi2_1_tt      = 0.0
    chi2_1_et      = 0.0
    chi2_1_te_frac = 0.0
    chi2_1_ee_frac = 0.0
    chi2_1_te_fid  = 0.0
    chi2_1_ee_fid  = 0.0

    chi2_2_tt      = 0.0
    chi2_2_et      = 0.0
    chi2_2_te_frac = 0.0
    chi2_2_ee_frac = 0.0
    chi2_2_te_fid  = 0.0
    chi2_2_ee_fid  = 0.0


    # Calculate correlation matrix for each l.o.s.
    for ID in ID_list:

        # Load stats for model 0 (fiducial)
        mock_file = mod0_dir + 'stats_' + ID + '.dat'
        mm_mean_0, std_0 = np.genfromtxt(mock_file, unpack=True, usecols=[0,2])

        # Load weighted random counts for model 0
        w_10_file = pairs0_dir + 'mm_10_' + ID + '.dat'
        mm_0 = np.genfromtxt(w_10_file)

        # Load stats for model 1
        mock_file = mod1_dir + 'stats_' + ID + '.dat'
        mm_mean_1, std_1 = np.genfromtxt(mock_file, unpack=True, usecols=[0,2])

        # Load weighted random counts for model 1
        w_10_file = pairs1_dir + 'mm_10_' + ID + '.dat'
        mm_1 = np.genfromtxt(w_10_file)

        # Load stats for model 2
        mock_file = mod2_dir + 'stats_' + ID + '.dat'
        mm_mean_2, std_2 = np.genfromtxt(mock_file, unpack=True, usecols=[0,2])

        # Load weighted random counts for model 2
        w_10_file = pairs2_dir + 'mm_10_' + ID + '.dat'
        mm_2 = np.genfromtxt(w_10_file)

        # Load dd counts from one mock
        dd_file = dd_dir + 'dd_' + ID + '.dat'
        dd = np.genfromtxt(dd_file)


        for i in range(len(dd)):
            if dd[i]==0.0: continue
            DD = dd[i]
            chi2_0_tt += ( (mm_mean_0[i] - DD) / std_0[i] )**2
            chi2_1_tt += ( (mm_mean_1[i] - DD) / std_1[i] )**2
            chi2_2_tt += ( (mm_mean_2[i] - DD) / std_2[i] )**2


    print(chi2_0_tt, chi2_1_tt, chi2_2_tt)


        # plt.close()
        # plt.clf()
        # xmin = min(bin_centers)
        # xmax = max(bin_centers)
        # ymin = -1
        # ymax = 1

        # plt.title('Real mean (' + N_mocks + ' mocks) vs. weighted mean l.o.s. ' + ID, fontsize=20)
        # plt.xlabel('Bin Center (kpc)', fontsize=18)
        # plt.ylabel(r'$\frac{MM_{weighted}-MM_{mean}}{\sigma}$', fontsize=18)
        # # plt.ylabel(r'$\frac{MM_{weighted}-MM_{mean}}{MM_{mean}}$', fontsize=18)
        # # plt.semilogx(bin_centers, dd_mean, color='#CC4F1B')
        # # plt.semilogx(bin_centers, dd_weighted, color='black')
        # # plt.fill_between(bin_centers, dd_mean-std, dd_mean+std, alpha=0.5, edgecolor='#CC4F1B',
        # #     facecolor='#FF9848')
        # plt.semilogx(bin_centers, excess_10, color='black')
        # plt.semilogx(bin_centers, excess_50, color='green')
        # plt.semilogx(bin_centers, excess_100, color='blue')
        # plt.semilogx(bin_centers, excess_1000, color='red')
        # plt.axis([xmin, xmax, ymin, ymax])
        # plt.legend(handles=[black_patch, green_patch, blue_patch, red_patch], loc='upper left')
        # fig_name = plots_dir + 'real_vs_weighted_' + N_mocks + '_' + ID + '.png'
        # plt.savefig(fig_name)
        # png_list.append(fig_name)


if __name__ == '__main__':
    main()