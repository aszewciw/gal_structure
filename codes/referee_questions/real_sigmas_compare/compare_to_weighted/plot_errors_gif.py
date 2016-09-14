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
    bins_file   = rbins_dir + 'rbins.ascii.dat'
    bin_centers = np.genfromtxt(bins_file, skip_header=1, usecols=[2], unpack=True)
    N_bins      = len(bin_centers)

    # Round bin centers to three decimal places
    bin_centers = np.round(bin_centers, 3)

    # Create list of png's for use in making gif
    # png_std_list =[]
    # png_frac_list =[]
    png_list = []

    red_patch = mpatches.Patch(color='red', label=r'$DD_{mean}$')
    blue_patch = mpatches.Patch(color='blue', label=r'$DD_{weighted}$')

    # Calculate correlation matrix for each l.o.s.
    for ID in ID_list:

        # if ID != '0':
        #     continue

        mock_file = mock_dir + 'stats_' + ID + '.dat'
        dd_mean, std = np.genfromtxt(mock_file, unpack=True, usecols=[0,2])

        weighted_file = data_dir + 'MWM_dd_' + ID + '.dat'
        dd_weighted = np.genfromtxt(weighted_file)

        plt.close()
        plt.clf()
        xmin = min(bin_centers)
        xmax = max(bin_centers)
        ymin = 0
        ymax = 0.5

        plt.title('Real mean vs. weighted mean l.o.s. ' + ID, fontsize=20)
        plt.xlabel('Bin Center (kpc)', fontsize=18)
        # plt.ylabel(r'$\frac{\sigma_{MM}/MM}{\sigma_{RR}/RR}$', fontsize=24)
        plt.ylabel('Normalized DD', fontsize=24)
        plt.semilogx(bin_centers, dd_mean, color='red')
        plt.semilogx(bin_centers, dd_weighted, color='blue')
        plt.axis([xmin, xmax, ymin, ymax])
        plt.legend(handles=[red_patch, blue_patch], loc='upper left')
        fig_name = plots_dir + 'real_vs_weighted_' + ID + '.png'
        plt.savefig(fig_name)
        png_list.append(fig_name)


    gif_name = plots_dir + 'real_vs_weighted.gif'
    GIF_MOVIE(png_list, gif_name)

if __name__ == '__main__':
    main()