from config import *
import matplotlib.pyplot as plt

def get_bias_sq(corr1, corr2):

    N_elements = len(corr1)

    bias_sq = np.zeros(N_elements)

    for i in range(N_elements):

        # Set bias=0 if empty value
        if (corr1[i]==0.0) or (corr2[i]==0.0):
            continue

        bias_sq[i] = corr1[i]/corr2[i]

    return(bias_sq)

def get_error(bias_sq, corr1, corr2, err1, err2):

    N_elements = len(bias_sq)

    error = np.zeros(N_elements)

    for i in range(N_elements):

        if (bias_sq[i]==0.0):
            continue

        temp1 = (err1[i] / corr1[i])**2
        temp2 = (err2[i] / corr2[i])**2
        temp3 = (temp1 + temp2) * (bias_sq[i]**2)

        error[i] = math.sqrt(temp3)


    return error



input_filename = data_dir + 'corr_list.dat'
sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
input_file     = open(input_filename, 'rb')
corr_list      = pickle.load(input_file)
input_file.close()

for p in corr_list:

    corr_file1 = data_dir + 'corr_full_10data_' + p.ID + '.dat'
    corr_file2 = data_dir + 'corr_full_10mock_' + p.ID + '.dat'
    corr_file3 = data_dir + 'corr_full_1500_' + p.ID + '.dat'
    corr_file4 = data_dir + 'corr_full_2000_' + p.ID + '.dat'

    bin_min, f_corr1 = np.genfromtxt(corr_file1, unpack=True, usecols=[0, 1])
    f_corr2 = np.genfromtxt(corr_file2, unpack=True, usecols=[1])
    f_corr3 = np.genfromtxt(corr_file3, unpack=True, usecols=[1])
    f_corr4 = np.genfromtxt(corr_file4, unpack=True, usecols=[1])

    error_file1 = data_dir + 'real_error_full_10data_' + p.ID + '.dat'
    error_file2 = data_dir + 'real_error_full_10mock_' + p.ID + '.dat'
    error_file3 = data_dir + 'real_error_full_1500_' + p.ID + '.dat'
    error_file4 = data_dir + 'real_error_full_2000_' + p.ID + '.dat'

    f_error1 = np.genfromtxt(error_file1)
    f_error2 = np.genfromtxt(error_file2)
    f_error3 = np.genfromtxt(error_file3)
    f_error4 = np.genfromtxt(error_file4)

    corr_file1 = data_dir + 'corr_cut_10data_' + p.ID + '.dat'
    corr_file2 = data_dir + 'corr_cut_10mock_' + p.ID + '.dat'
    corr_file3 = data_dir + 'corr_cut_1500_' + p.ID + '.dat'
    corr_file4 = data_dir + 'corr_cut_2000_' + p.ID + '.dat'

    c_corr1 = np.genfromtxt(corr_file1, unpack=True, usecols=[1])
    c_corr2 = np.genfromtxt(corr_file2, unpack=True, usecols=[1])
    c_corr3 = np.genfromtxt(corr_file3, unpack=True, usecols=[1])
    c_corr4 = np.genfromtxt(corr_file4, unpack=True, usecols=[1])

    error_file1 = data_dir + 'real_error_cut_10data_' + p.ID + '.dat'
    error_file2 = data_dir + 'real_error_cut_10mock_' + p.ID + '.dat'
    error_file3 = data_dir + 'real_error_cut_1500_' + p.ID + '.dat'
    error_file4 = data_dir + 'real_error_cut_2000_' + p.ID + '.dat'

    c_error1 = np.genfromtxt(error_file1)
    c_error2 = np.genfromtxt(error_file2)
    c_error3 = np.genfromtxt(error_file3)
    c_error4 = np.genfromtxt(error_file4)

    plt.clf()
    # plt.semilogx(bin_min, f_corr1, 'b')
    # plt.semilogx(bin_min, f_corr2, 'b')
    # plt.semilogx(bin_min, f_corr3, 'b')
    # plt.semilogx(bin_min, f_corr4, 'b')
    # plt.semilogx(bin_min, c_corr1, 'r')
    # plt.semilogx(bin_min, c_corr2, 'r')
    # plt.semilogx(bin_min, c_corr3, 'r')
    # plt.semilogx(bin_min, c_corr4, 'r')
    plt.errorbar(bin_min, f_corr1, yerr=f_error1, color='b', ecolor='b',
        elinewidth = 1.5, capthick = 1.5, capsize = 7)
    # plt.errorbar(bin_min, f_corr2, yerr=f_error2, color='b', ecolor='b',
    #     elinewidth = 1.5, capthick = 1.5, capsize = 7)
    # plt.errorbar(bin_min, f_corr3, yerr=f_error3, color='b', ecolor='b',
    #     elinewidth = 1.5, capthick = 1.5, capsize = 7)
    # plt.errorbar(bin_min, f_corr4, yerr=f_error4, color='b', ecolor='b',
    #     elinewidth = 1.5, capthick = 1.5, capsize = 7)
    plt.errorbar(bin_min, c_corr1, yerr=c_error1, color='r', ecolor='r',
        elinewidth = 1.5, capthick = 1.5, capsize = 7)
    # plt.errorbar(bin_min, c_corr2, yerr=c_error2, color='r', ecolor='r',
    #     elinewidth = 1.5, capthick = 1.5, capsize = 7)
    # plt.errorbar(bin_min, c_corr3, yerr=c_error3, color='r', ecolor='r',
    #     elinewidth = 1.5, capthick = 1.5, capsize = 7)
    # plt.errorbar(bin_min, c_corr4, yerr=c_error4, color='r', ecolor='r',
    #     elinewidth = 1.5, capthick = 1.5, capsize = 7)
    # plt.axis([0.004, 2, -1, 1.5])
    # plt.semilogx()

    # bias_sq = get_bias_sq(c_corr1, f_corr1)
    # bias_sq_error = get_error(bias_sq, c_corr1, f_corr1, c_error1, f_error1)
    # plt.errorbar(bin_min, bias_sq, yerr=bias_sq_error, fmt='o', color='b', ecolor='b',
    #     elinewidth = 1.5, capthick = 1.5, capsize = 7)

    # x = np.arange()

    # plt.plot(x,y,'r')


    # bias_sq = get_bias_sq(c_corr2, f_corr2)
    # bias_sq_error = get_error(bias_sq, c_corr2, f_corr2, c_error2, f_error2)
    # plt.errorbar(bin_min, bias_sq, yerr=bias_sq_error, color='r', ecolor='r',
    #     elinewidth = 1.5, capthick = 1.5, capsize = 7)

    # bias_sq = get_bias_sq(c_corr3, f_corr3)
    # bias_sq_error = get_error(bias_sq, c_corr3, f_corr3, c_error3, f_error3)
    # plt.errorbar(bin_min, bias_sq, yerr=bias_sq_error, color='k', ecolor='k',
    #     elinewidth = 1.5, capthick = 1.5, capsize = 7)

    # bias_sq = get_bias_sq(c_corr4, f_corr4)
    # bias_sq_error = get_error(bias_sq, c_corr4, f_corr4, c_error4, f_error4)
    # plt.errorbar(bin_min, bias_sq, yerr=bias_sq_error, color='g', ecolor='g',
    #     elinewidth = 1.5, capthick = 1.5, capsize = 7)

    plt.axis([0.004, 2, -1, 1.5])
    plt.semilogx()

    figure_name = plots_dir + 'fraction_' + p.ID + '.png'
    figure_name = plots_dir + 'correlation_' + p.ID + '.png'
    plt.savefig(figure_name)


