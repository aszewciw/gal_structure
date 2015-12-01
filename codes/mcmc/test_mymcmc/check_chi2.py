from config import *

'''This will be the main mcmc loop. I assume
that I have already counted all pairs in all
lines of site for data and random. I have
one file for each random sample storing pair
counts (Z_i, R_i, w_i, Z_j, R_j, w_j). The
plan is to load all 152 of these into 152
separate dictionaries. I also have the
jackknife errors for this catalogue already.
I should note that the data correlation only
needs to be calculated once (and it has).'''



#############################################################

# @profile
def chi2(todo_list, N_files, MODEL):

    '''Calculates chi-square for given model'''

    chi2 = []
    sig2 = []
    DDMM = []

    for p in todo_list:

        plate = int(p.ID)
        if plate >= N_files:
            continue

        los = 'los_' + p.ID

        DDMM_array = MODEL[los]['DD/MM']
        sig2_array = ( DDMM_array ** 2 ) * MODEL[los]['err2_temp']
        chi2_array = ( DDMM_array - 1 )**2  * ( sig2_array ** -1 )

        for j in range(len(chi2_array)):
            chi2.append(chi2_array[j])
            sig2.append(sig2_array[j])
            DDMM.append(DDMM_array[j])

    return(chi2, sig2, DDMM)


#############################################################

#############################################################

# @profile
def main():

    np.random.seed()

    ####################_PARAMETERS_########################

    N_acc    = 0    # Number of accepted steps
    MCMC_eff = 0    # accepted / total
    N_dof    = 0    # degrees of freedom
    N_params = 5
    N_dof    -= N_params


    elements_needed = int(5)

    args_array = np.array(sys.argv)
    N_args = len(args_array)
    assert(N_args == elements_needed)
    N_loops = int(args_array[1])
    N_files = int(args_array[2])
    outfile = args_array[3]
    N_std = int(args_array[4])

    ####################_PARAMETERS_########################


    ###################_INITIALIZATION_#####################

    MODEL    = {}
    DATA     = {}
    MODEL_ZR = {}

    # Lists to be filled so I can see wtf is wrong with chi2
    MM = []
    LOS = []

    ###################_INITIALIZATION_#####################


    ####################_DATA_INPUT_########################

    # Lines of sight

    input_filename = rawdata_dir + 'todo_list.dat'
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()
    N_los          = len(todo_list)


    # Loading data into dictionaries and subdictionaries
    for p in todo_list:

        # Limit number of los
        plate = int(p.ID)
        if plate >= N_files:
            continue

        print('Loading Pointing #', p.ID)

        # Subdictionaries for each los
        los           = 'los_' + p.ID
        MODEL[los]    = {}
        MODEL_ZR[los] = {}

        # File containing ascii data for uniform samples (has Z and R; W is 1)
        ZR_file = uni_dir + 'uniform_' + p.ID + '.ascii.dat'

        MODEL_ZR[los]['Z'], MODEL_ZR[los]['R'], = np.genfromtxt(
            ZR_file, unpack=True, skiprows=1, usecols=[5, 6], dtype=None)

        # Load jackknife errors as numpy arrays: one error for each bin
        uni_jk_file             = jk_dir + 'uniform_' + p.ID + '_jk_error.dat'
        uni_jk_err              = np.genfromtxt(uni_jk_file, unpack=True, usecols=[7])
        dat_jk_file             = jk_dir + 'mock_' + p.ID + '_jk_error.dat'
        dat_jk_err              = np.genfromtxt(dat_jk_file, unpack=True, usecols=[7])
        MODEL[los]['err2_temp'] = uni_jk_err ** 2 + dat_jk_err ** 2
        #Multiply err2_temp by DD/MM **2 to get sigma2 in DD/MM

        # Load normalized and weighted DD counts
        DD_file         = mock_dir + 'DD_' + p.ID + '.dat'
        MODEL[los]['DD'] = np.genfromtxt(DD_file, usecols=[2])


        for j in range(Nbins):

            BIN             = 'bin_' + str(j)

            MODEL[los][BIN] = {}

            model_file      = uni_dir + 'counts_' + p.ID + '.bin_' + str(j + 1) + '.dat'

            MODEL[los][BIN]['ind1'], MODEL[los][BIN]['ind2'] = np.genfromtxt(
                model_file, dtype=None, unpack=True)


    ####################_DATA_INPUT_########################


    #################_MODEL_INITIALIZATION_#################

    # Weight model points and calculate DD/MM

    for p in todo_list:

        plate = int(p.ID)
        if plate >= N_files:
            continue


        los = 'los_' + p.ID

        weight = ( ( ( np.cosh(MODEL_ZR[los]['Z'] * ( 2 * z_thin ) ** (-1) ) ) ** (-2) )
            * np.exp(-MODEL_ZR[los]['R'] * (r_thin ** -1)) +
            a * ( ( np.cosh(MODEL_ZR[los]['Z'] * (2 * z_thick ** (-1) ) ) ** (-2) )
            * np.exp(-MODEL_ZR[los]['R'] * r_thick ** -1) ) )

        norm = ( np.sum(weight) ** 2 - np.inner(weight, weight)) / 2

        MM_temp = np.zeros(Nbins)
        DD      = MODEL[los]['DD']
        DD_MM   = np.ones(Nbins)   # Set as 1 to start. If DD/MM = 1, then no contribution to chi2.

        for j in range(Nbins):

            BIN = 'bin_' + str(j)

            if DD[j] > 0:

                MM_temp[j] = np.sum( weight[MODEL[los][BIN]['ind1']] *
                    weight[MODEL[los][BIN]['ind2']] ) * (norm ** -1)

                if MM_temp[j] <=0:
                    continue
                else:
                    DD_MM[j] = DD[j] / MM_temp[j]
                    N_dof += 1

            MM.append(MM_temp[j])
            LOS.append(plate)

        MODEL[los]['DD/MM'] = DD_MM


    print('Number of degrees of freedom: ', N_dof, '\n')
    # Calculate initial chi2

    CHI2, SIG2, DDMM = chi2(todo_list, N_files, MODEL)

    #################_MODEL_INITIALIZATION_#################


    ########################_MCMC_##########################

    # k = 1   # start loop index at 1 because of initialization

    # while k < (N_loops):

    #     print('Loop number: ', k)

    #     # Assign new params
    #     A[k], Z_THICK[k], R_THICK[k], Z_THIN[k], R_THIN[k] = assign_params(
    #         A[k-1], Z_THICK[k-1], R_THICK[k-1], Z_THIN[k-1], R_THIN[k-1])

    #     for p in todo_list:

    #         plate = int(p.ID)
    #         if plate >= N_files:
    #             continue

    #         los = 'los_' + p.ID

    #         weight = ( ( ( np.cosh(MODEL_ZR[los]['Z'] * ( 2 * Z_THIN[k] ) ** (-1) ) ) ** (-2) )
    #             * np.exp(-MODEL_ZR[los]['R'] * (R_THIN[k] ** -1)) +
    #             A[k] * ( ( np.cosh(MODEL_ZR[los]['Z'] * (2 * Z_THICK[k]) ** (-1) ) ) ** (-2) )
    #             * np.exp(-MODEL_ZR[los]['R'] * R_THICK[k] ** -1) )

    #         # MODEL_ZRW[los]['norm'] = norm_weights(MODEL_ZRW[los]['W'])
    #         norm = ( np.sum(weight) ** 2 - np.inner(weight, weight) ) / 2

    #         MM_temp = np.zeros(Nbins)
    #         DD      = MODEL[los]['DD']
    #         DD_MM   = np.ones(Nbins)   # Set as 1 to start. If DD/MM = 1, then no contribution to chi2.

    #         # This should maybe be replaced with list comprehension if possible
    #         for j in range(Nbins):

    #             BIN = 'bin_' + str(j)

    #             if DD[j] > 0:

    #                 MM_temp[j] = np.sum( weight[MODEL[los][BIN]['ind1']] *
    #                     weight[MODEL[los][BIN]['ind2']] ) * (norm ** -1)

    #                 if MM_temp[j] <=0:
    #                     continue
    #                 else:
    #                     DD_MM[j] = DD[j] / MM_temp[j]


    #         MODEL[los]['DD/MM'] = DD_MM


    #     CHI2[k]    = chi2(todo_list, N_files, MODEL)
    #     CHI2_TEST[k] = CHI2[k]

    #     delta_chi2 = CHI2[k] - CHI2[k - 1]


    #     if delta_chi2 < 0:

    #         N_acc += 1

    #     else:

    #         rnd = random.random()

    #         test = math.exp(-delta_chi2 / 2)

    #         if rnd < test:

    #             N_acc += 1

    #         else:

    #             CHI2[k]    = CHI2[k-1]
    #             A[k]       = A[k-1]
    #             Z_THICK[k] = Z_THICK[k-1]
    #             Z_THIN[k]  = Z_THIN[k-1]
    #             R_THICK[k] = R_THICK[k-1]
    #             R_THIN[k]  = R_THIN[k-1]

    #     EFF[k] = N_acc / k
    #     k += 1

    np.savez(outfile, CHI2=CHI2, LOS=LOS, MM=MM, SIG2=SIG2, DDMM=DDMM)

    print('MCMC done. Data output to: ', outfile)

if __name__ == '__main__':
    main()