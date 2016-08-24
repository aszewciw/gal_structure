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
    png_list =[]

    # Calculate correlation matrix for each l.o.s.
    for ID in ID_list:

        # Load RR fractional errors
        RR_filename = data_dir + 'uniform_' + ID + '_jk_error.dat'
        RR_frac_err = np.genfromtxt(RR_filename, unpack=True, usecols=[7])

        # Load MM_0 fractional errors
        MM_0_filename = data_dir + 'MWM_type0_' + ID + '_jk_error.dat'
        MM_0_frac_err = np.genfromtxt(MM_0_filename, unpack=True, usecols=[7])

        # Load MM_1 fractional errors
        MM_1_filename = data_dir + 'MWM_type1_' + ID + '_jk_error.dat'
        MM_1_frac_err = np.genfromtxt(MM_1_filename, unpack=True, usecols=[7])

        # Initialize ratio arrays
        ratio_MM_0_RR = np.zeros(N_bins)
        ratio_MM_1_RR = np.zeros(N_bins)

        for i in range(N_bins):
            if(RR_frac_err[i] == 0.0):
                continue
            ratio_MM_0_RR[i] = MM_0_frac_err[i] / RR_frac_err[i]
            ratio_MM_1_RR[i] = MM_1_frac_err[i] / RR_frac_err[i]

        plt.close()
        plt.clf()
        xmin = min(bin_centers)
        xmax = max(bin_centers)
        ymin = 0
        ymax = 5

        plt.title('Fractional error ratios for l.o.s. ' + ID, fontsize=20)
        plt.xlabel('Bin Center (kpc)', fontsize=18)
        plt.ylabel(r'$\frac{\sigma_{MM}/MM}{\sigma_{RR}/RR}$', fontsize=24)
        plt.semilogx(bin_centers, ratio_MM_0_RR, color='red')
        plt.semilogx(bin_centers, ratio_MM_1_RR, color='blue')
        plt.axis([xmin, xmax, ymin, ymax])
        fig_name = plots_dir + 'frac_error_ratio_' + ID + '.png'
        plt.savefig(fig_name)
        png_list.append(fig_name)

    gif_name = plots_dir + 'error_ratios.gif'
    GIF_MOVIE(png_list, gif_name)

if __name__ == '__main__':
    main()