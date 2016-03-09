from config import *

'''
Using my mcmc code (with some modifications) to calculate
chi2 for Qingqing's best fit found from this file:

/fs1/szewciw/gal_structure/codes/mcmc/compare_chi2_qiqi/
    debugging_March/data/mcmc_2disks_model.dat

His chi2 value is also found in that file.

'''

def chi2(todo_list, MODEL):

    '''Calculates chi-square for given model'''

    chi2 = 0
    DOF = 0
    chi2_list = []

    for p in todo_list:

        los = 'los_' + p.ID

        DD_MM = MODEL[los]['DD/MM']
        sig2  = ( DD_MM ** 2 ) * MODEL[los]['err2_temp']

        for i in range(len(DD_MM)):

            if DD_MM[i] <= 0.0 or sig2[i] <= 0.0:
                chi2_list.append(0)
                continue

            DOF += 1
            chi2_temp = (DD_MM[i] - 1)**2 * (sig2[i] ** -1)
            chi2_list.append(chi2_temp)
            chi2 += chi2_temp
    print('Chi2 is: ', chi2)

    return chi2_list, DOF


#############################################################

#############################################################

def main():

    np.random.seed()

    ####################_PARAMETERS_########################

    elements_needed = int(2)

    args_array    = np.array(sys.argv)
    N_args        = len(args_array)
    assert(N_args == elements_needed)
    outfile       = args_array[1]
    outfile       = out_dir + outfile

    MODEL    = {}
    MODEL_ZR = {}


    # Lines of sight

    input_filename = rawdata_dir + 'todo_list.dat'
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()
    N_los          = len(todo_list)

    #Quantities to save
    LOS_NUM      = []
    BIN_NUM      = []
    UNI_JK_ERR   = []
    DAT_JK_ERR   = []
    ERR2_TEMP    = []
    DD           = []
    MM           = []


    # Loading data into dictionaries and subdictionaries
    for p in todo_list:

        print('Loading Pointing #', p.ID)

        # Subdictionaries for each los
        los           = 'los_' + p.ID
        MODEL[los]    = {}
        MODEL_ZR[los] = {}

        '''Commented out because I know MM'''
        # File containing ascii data for uniform samples (has Z and R; W is 1)
        # ZR_file = qiqi_dir + 'uniform_' + p.ID + '.ascii.dat'

        # MODEL_ZR[los]['Z'], MODEL_ZR[los]['R'], = np.genfromtxt(
        #     ZR_file, unpack=True, skip_header=1, usecols=[5, 6], dtype=None)
        '''End commenting'''

        # Load jackknife errors as numpy arrays: one error for each bin
        uni_jk_file             = qiqi_dir + 'uniform_' + p.ID + '_jk_error.dat'
        uni_jk_err              = np.genfromtxt(uni_jk_file, unpack=True, usecols=[7])
        dat_jk_file             = qiqi_dir + 'star_' + p.ID + '_jk_error.dat'
        dat_jk_err              = np.genfromtxt(dat_jk_file, unpack=True, usecols=[7])

        # Set combined error at zero initially. Skip los if either jk error is 0.
        err2_temp = np.zeros(len(dat_jk_err))

        for i in range(len(err2_temp)):

            UNI_JK_ERR.append(uni_jk_err[i])
            DAT_JK_ERR.append(dat_jk_err[i])
            LOS_NUM.append(int(p.ID))
            BIN_NUM.append(i + 1)

            if uni_jk_err[i] == 0.0 or dat_jk_err[i] == 0.0:
                continue
            err2_temp[i] = uni_jk_err[i] ** 2 + dat_jk_err[i] ** 2

        MODEL[los]['err2_temp'] = err2_temp
        for i in range(len(err2_temp)):
            ERR2_TEMP.append(err2_temp[i])


        #Multiply err2_temp by DD/MM **2 to get sigma2 in DD/MM

        # Load normalized and weighted DD counts
        DD_file          = DD_dir + 'DD_' + p.ID + '.dat'
        MODEL[los]['DD'] = np.genfromtxt(DD_file, usecols=[2], unpack=True)

        '''Commented out because I know MM'''

        # for j in range(Nbins):

        #     BIN             = 'bin_' + str(j)

        #     MODEL[los][BIN] = {}

        #     model_file      = model_dir + 'counts_' + p.ID + '.bin_' + str(j + 1) + '.dat'

        #     MODEL[los][BIN]['ind1'], MODEL[los][BIN]['ind2'] = np.genfromtxt(
        #         model_file, dtype=None, unpack=True)


        # weight = ( ( ( np.cosh(MODEL_ZR[los]['Z'] * ( 2 * z_thin ) ** (-1) ) ) ** (-2) )
        #     * np.exp(-MODEL_ZR[los]['R'] * (r_thin ** -1)) +
        #     a * ( ( np.cosh(MODEL_ZR[los]['Z'] * (2 * z_thick) ** (-1) ) ) ** (-2) )
        #     * np.exp(-MODEL_ZR[los]['R'] * r_thick ** -1) )

        # MODEL_ZRW[los]['norm'] = norm_weights(MODEL_ZRW[los]['W'])
        # norm    = ( np.sum(weight) ** 2 - np.inner(weight, weight) ) / 2

        # MM_temp = np.zeros(Nbins)
        # DD_MM   = np.zeros(Nbins)

        # for j in range(Nbins):

        #     BIN = 'bin_' + str(j)

        #     DD.append(MODEL[los]['DD'][j])

        #     if MODEL[los]['DD'][j] <= 0.0:

        #         continue

        #     MM_temp[j] = np.sum( weight[MODEL[los][BIN]['ind1']] *
        #         weight[MODEL[los][BIN]['ind2']] ) * (norm ** -1)

        #     MM.append(MM_temp[j])

        #     if MM_temp[j] <=0:
        #         continue

        #     DD_MM[j] = MODEL[los]['DD'][j] / MM_temp[j]

        # MODEL[los]['DD/MM'] = DD_MM
        '''End commenting'''

        '''Adding in new lines because I know MM'''

        MM_file = weighted_dir + 'MM_' + p.ID + '.dat'
        MM_temp = np.genfromtxt(MM_file, unpack=True, usecols=[2])
        DD_MM   = np.zeros(Nbins)


        for j in range(Nbins):

            BIN = 'bin_' + str(j)

            DD.append(MODEL[los]['DD'][j])
            MM.append(MM_temp[j])

            if MODEL[los]['DD'][j] <= 0.0:

                continue

            if MM_temp[j] <= 0.0:
                continue

            DD_MM[j] = MODEL[los]['DD'][j] / MM_temp[j]

        MODEL[los]['DD/MM'] = DD_MM


    CHI2_LOS_BIN, N_dof = chi2(todo_list, MODEL)
    N_dof -= 5

    print('Degrees of Freedom: ', N_dof)

    np.savez(outfile, CHI2_LOS_BIN=CHI2_LOS_BIN, MM=MM, DD=DD, LOS_NUM=LOS_NUM,
        BIN_NUM=BIN_NUM, UNI_JK_ERR=UNI_JK_ERR, DAT_JK_ERR=DAT_JK_ERR)

    print('Test done. Data output to: ', outfile)

if __name__ == '__main__':
    main()
