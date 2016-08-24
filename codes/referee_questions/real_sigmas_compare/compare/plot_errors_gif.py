from config import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------#
'''
Produce a correlation matrix plot for each SEGUE l.o.s. using 1000 mocks.
Make a gif from the files.
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

def main():

    # Load list of pointing IDs
    todo_file = rawdata_dir + 'todo_list.ascii.dat'
    ID_list   = np.genfromtxt(todo_file, skip_header=1, usecols=[0], unpack=True,
                            dtype=str)
    N_los = len(ID_list)

    # Load bins centers
    bins_file   = data_dir + 'rbins.ascii.dat'
    bin_centers = np.genfromtxt(bins_file, skip_header=1, usecols=[2], unpack=True)
    N_bins      = len(bin_centers)

    # Round bin centers to three decimal places
    bin_centers = np.round(bin_centers, 3)

    # Create list of png's for use in making gif
    png_std_list =[]
    png_frac_list =[]

    # Calculate correlation matrix for each l.o.s.
    for ID in ID_list:

        if int(ID) > 3:
            continue

        mock0_file = mock0_dir + 'stats_' + ID + '.dat'
        dd_0, std_0 = np.genfromtxt(mock0_file, unpack=True, usecols=[0,1])

        mock1_file = mock1_dir + 'stats_' + ID + '.dat'
        dd_1, std_1 = np.genfromtxt(mock1_file, unpack=True, usecols=[0,1])

        mock2_file = mock2_dir + 'stats_' + ID + '.dat'
        dd_2, std_2 = np.genfromtxt(mock2_file, unpack=True, usecols=[0,1])

        # Initialize ratio arrays
        # std_ratio_10 = np.zeros(N_bins)
        # std_ratio_20 = np.zeros(N_bins)

        # Initialize fractional ratio arrays
        frac_0 = np.zeros(N_bins)
        frac_1 = np.zeros(N_bins)
        frac_2 = np.zeros(N_bins)
        # frac_ratio_10 = np.zeros(N_bins)
        # frac_ratio_20 = np.zeros(N_bins)

        # Fill std ratios
        # for i in range(N_bins):
        #     if(std_0[i] == 0.0):
        #         continue
        #     std_ratio_10[i] = std_1[i] / std_0[i]
        #     std_ratio_20[i] = std_2[i] / std_0[i]

        for i in range(N_bins):
            if(dd_0[i] > 0.0):
                frac_0[i] = std_0[i] / dd_0[i]
            if(dd_1[i] > 0.0):
                frac_1[i] = std_1[i] / dd_1[i]
            if(dd_2[i] > 0.0):
                frac_2[i] = std_2[i] / dd_2[i]

        # for i in range(N_bins):
        #     if(frac_0[i] == 0.0):
        #         continue
        #     frac_ratio_10[i] = frac_1[i] / frac_0[i]
        #     frac_ratio_20[i] = frac_2[i] / frac_0[i]

        plt.close()
        plt.clf()
        xmin = min(bin_centers)
        xmax = max(bin_centers)
        ymin = 0
        ymax = 0.001

        plt.title('Sigma ratios (different parameters) l.o.s. ' + ID, fontsize=20)
        plt.xlabel('Bin Center (kpc)', fontsize=18)
        # plt.ylabel(r'$\frac{\sigma_{MM}/MM}{\sigma_{RR}/RR}$', fontsize=24)
        plt.ylabel(r'$\sigma_{DD}$', fontsize=24)
        plt.loglog(bin_centers, std_0, color='red')
        plt.loglog(bin_centers, std_1, color='blue')
        plt.loglog(bin_centers, std_2, color='green')
        plt.axis([xmin, xmax, ymin, ymax])
        fig_name = plots_dir + 'std_ratio_' + ID + '.png'
        plt.savefig(fig_name)
        png_std_list.append(fig_name)


        ymin = 0
        ymax = 5

        plt.title('Fractional error ratios (different parameters) l.o.s. ' + ID, fontsize=20)
        plt.xlabel('Bin Center (kpc)', fontsize=18)
        # plt.ylabel(r'$\frac{\sigma_{MM}/MM}{\sigma_{RR}/RR}$', fontsize=24)
        plt.ylabel(r'$\frac{\sigma_{DD}}{DD}$', fontsize=24)
        plt.semilogx(bin_centers, frac_0, color='red')
        plt.semilogx(bin_centers, frac_1, color='blue')
        plt.semilogx(bin_centers, frac_2, color='green')
        plt.axis([xmin, xmax, ymin, ymax])
        fig_name = plots_dir + 'frac_ratio_' + ID + '.png'
        plt.savefig(fig_name)
        png_frac_list.append(fig_name)

    # gif_name = plots_dir + 'error_ratios.gif'
    # GIF_MOVIE(png_list, gif_name)

if __name__ == '__main__':
    main()