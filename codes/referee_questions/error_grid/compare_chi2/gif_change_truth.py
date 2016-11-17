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

    z0_thin = [183, 193, 203, 213, 223, 233, 243, 253, 263, 273, 283, 293, 303, 313, 323]

    png_list = []
    png_frac_list = []

    for z in z0_thin:

        z = str(z)
        if z=='233': z='fid'

        dd_dir = '../500_mocks_' + z + '/errors_pairs/data/mock_' + mock_num + '/'

        chi2_true = np.zeros(len(z0_thin))
        chi2_uni  = np.zeros(len(z0_thin))
        chi2_nonuni = np.zeros(len(z0_thin))

        # Calculate correlation matrix for each l.o.s.
        for ID in ID_list:

            # Load dd counts from whichever model we deemed "truth"
            dd_file = dd_dir + 'mock_pairs_' + ID + '.dat'
            dd = np.genfromtxt(dd_file, unpack=True, usecols=[5])

            mocks_fid_dir = '../500_mocks_fid/errors_pairs/data/mean_var_std/'
            mock_fid_file = mocks_fid_dir + 'stats_' + ID + '.dat'
            mm_mean_fid, std_fid = np.genfromtxt(mock_fid_file, unpack=True, usecols=[0,2])

            frac_std = std_fid / mm_mean_fid

            for j in range(len(z0_thin)):

                Z = str(z0_thin[j])

                if Z=='233': Z='fid'

                mocks_dir = '../500_mocks_' + Z + '/errors_pairs/data/mean_var_std/'
                mock_file = mocks_dir + 'stats_' + ID + '.dat'
                mm_mean, std = np.genfromtxt(mock_file, unpack=True, usecols=[0,2])

                pairs_dir = '../pair_count_' + Z + '/data/'
                uni_file = pairs_dir + 'mm_uni_' + ID + '.dat'
                mm_uni = np.genfromtxt(uni_file)

                nonuni_file = pairs_dir + 'mm_nonuni_' + ID + '.dat'
                mm_nonuni = np.genfromtxt(nonuni_file)


                for i in range(len(dd)):

                    if dd[i]==0.0: continue
                    DD = dd[i]

                    # True true
                    chi2_true[j] += ( (mm_mean[i] - DD) / std[i] )**2

                    # uniform estimate
                    std_est = mm_uni[i] * frac_std[i]
                    chi2_uni[j] += ( (mm_uni[i] - DD) / std_est )**2

                    # nonuniform estimate
                    std_est = mm_nonuni[i] * frac_std[i]
                    chi2_nonuni[j] += ( (mm_nonuni[i] - DD) / std_est )**2


        chi2_uni_frac = (chi2_uni - chi2_true) / chi2_true
        chi2_nonuni_frac = (chi2_nonuni - chi2_true) / chi2_true

        z0 = np.asarray(z0_thin)
        z0 = z0/1000.0

        plt.clf()
        plt.figure(1)
        plt.xlabel('z0_{thin}')
        plt.ylabel(r'$\frac{(\chi_{est}^2-\chi_{true}^2)}{\chi_{true}^2}$',fontsize=20)
        plt.plot(z0, chi2_uni_frac, marker='*', label='uniform')
        plt.plot(z0, chi2_nonuni_frac, marker='^', label='nonuniform')
        plt.legend(numpoints=1, loc='upper left')
        plt.tight_layout()
        fig_name = plots_dir + 'chi2_frac_z' + z + '_m' + mock_num + '.png'
        plt.savefig(fig_name)
        png_frac_list.append(fig_name)

        plt.clf()
        plt.figure(2)
        plt.xlabel('z0_{thin}')
        plt.ylabel(r'$\chi^2$')
        plt.plot(z0, chi2_uni, marker='*', label='uniform')
        plt.plot(z0, chi2_nonuni, marker='^', label='nonuniform')
        plt.plot(z0, chi2_true, marker='s', label='true')
        plt.legend(numpoints=1, loc='upper left')
        plt.tight_layout()
        fig_name = plots_dir + 'chi2_z' + z + '_m' + mock_num + '.png'
        plt.savefig(fig_name)
        png_list.append(fig_name)

    frac_gif = plots_dir + 'chi2_frac_m' + mock_num + '.gif'
    chi2_gif = plots_dir + 'chi2_m' + mock_num + '.gif'

    GIF_MOVIE(png_frac_list, frac_gif, removef=True)
    GIF_MOVIE(png_list, chi2_gif, removef=True)

if __name__ == '__main__':
    main()