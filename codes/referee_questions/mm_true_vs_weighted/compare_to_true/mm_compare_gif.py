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

    # CL Input
    elements_needed = int(2)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args == elements_needed)
    N_mocks = args_array[1]

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

    org_patch = mpatches.Patch(color='#CC4F1B', label=r'$MM_{mean}$')
    black_patch = mpatches.Patch(color='black', label=r'$MM_{10}$')
    green_patch = mpatches.Patch(color='green', label=r'$MM_{50}$')
    blue_patch = mpatches.Patch(color='blue', label=r'$MM_{100}$')
    red_patch = mpatches.Patch(color='red', label=r'$MM_{1000}$')

    # Calculate correlation matrix for each l.o.s.
    for ID in ID_list:

        if int(ID) > 50:
            continue

        mock_file = mock1000_dir + 'stats_' + ID + '.dat'
        dd_mean, std = np.genfromtxt(mock_file, unpack=True, usecols=[0,2])

        w_10_file = pairs_dir + 'mm_10_' + ID + '.dat'
        dd_10 = np.genfromtxt(w_10_file)
        excess_10 = (dd_10 - dd_mean) / std
        # excess_10 = (dd_10 - dd_mean) / dd_mean

        w_50_file = pairs_dir + 'mm_50_' + ID + '.dat'
        dd_50 = np.genfromtxt(w_50_file)
        excess_50 = (dd_50 - dd_mean) / std
        # excess_50 = (dd_50 - dd_mean) / dd_mean

        w_100_file = pairs_dir + 'mm_100_' + ID + '.dat'
        dd_100 = np.genfromtxt(w_100_file)
        excess_100 = (dd_100 - dd_mean) / std
        # excess_100 = (dd_100 - dd_mean) / dd_mean

        w_1000_file = pairs_dir + 'mm_1000_' + ID + '.dat'
        dd_1000 = np.genfromtxt(w_1000_file)
        excess_1000 = (dd_1000 - dd_mean) / std
        # excess_1000 = (dd_1000 - dd_mean) / dd_mean

        plt.close()
        plt.clf()
        xmin = min(bin_centers)
        xmax = max(bin_centers)
        ymin = -1
        ymax = 1

        plt.title('Real mean (' + N_mocks + ' mocks) vs. weighted mean l.o.s. ' + ID, fontsize=20)
        plt.xlabel('Bin Center (kpc)', fontsize=18)
        # plt.ylabel(r'$\frac{MM_{weighted}-MM_{mean}}{\sigma}$', fontsize=18)
        plt.ylabel(r'$\frac{MM_{weighted}-MM_{mean}}{MM_{mean}}$', fontsize=18)
        # plt.semilogx(bin_centers, dd_mean, color='#CC4F1B')
        # plt.semilogx(bin_centers, dd_weighted, color='black')
        # plt.fill_between(bin_centers, dd_mean-std, dd_mean+std, alpha=0.5, edgecolor='#CC4F1B',
        #     facecolor='#FF9848')
        plt.semilogx(bin_centers, excess_10, color='black')
        plt.semilogx(bin_centers, excess_50, color='green')
        plt.semilogx(bin_centers, excess_100, color='blue')
        plt.semilogx(bin_centers, excess_1000, color='red')
        plt.axis([xmin, xmax, ymin, ymax])
        plt.legend(handles=[black_patch, green_patch, blue_patch, red_patch], loc='upper left')
        fig_name = plots_dir + 'real_vs_weighted_' + N_mocks + '_' + ID + '.png'
        plt.savefig(fig_name)
        png_list.append(fig_name)


    gif_name = plots_dir + 'real_vs_weighted_' + N_mocks + '.gif'
    GIF_MOVIE(png_list, gif_name, removef=True)

if __name__ == '__main__':
    main()