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


def assign_params(a, z_thick, r_thick, z_thin, r_thin, init=1, N_std=0):

    '''
    Assigns new parameters based on current values
    and "known" standard deviation from Mao et. al.
    init will have value 0 if we are initializing
    values.
    '''

    a_std     = 0.002
    z_thick_std = 0.005
    r_thick_std = 0.05
    z_thin_std = 0.005
    r_thin_std = 0.05

    if init == 0:

        a       += N_std * a_std
        z_thick += N_std * z_thick_std
        r_thick += N_std * r_thick_std
        z_thin  += N_std * z_thin_std
        r_thin  += N_std * r_thin_std

    else:

        a       = np.random.normal(a, a_std)
        z_thick = np.random.normal(z_thick, z_thick_std)
        r_thick = np.random.normal(r_thick, r_thick_std)
        z_thin  = np.random.normal(z_thin, z_thin_std)
        r_thin  = np.random.normal(r_thin, r_thin_std)

    return(a, z_thick, r_thick, z_thin, r_thin)

#############################################################

#############################################################

# @profile
def chi2(todo_list, N_files, MODEL):

    '''Calculates chi-square for given model'''

    chi2 = 0

    # for p in todo_list:

    #     plate = int(p.ID)
    #     if plate >= N_files:
    #         continue

    #     los = 'los_' + p.ID

    #     DD_MM = MODEL[los]['DD/MM']
    #     sig2  = ( DD_MM ** 2 ) * MODEL[los]['err2_temp']

    #     for i in range(len(DD_MM)):

    #         if DD_MM[i] <= 0.0:
    #             continue

    #         chi2 += (DD_MM[i] - 1)**2 * (sig2[i] ** -1)
    for p in todo_list:

        plate = int(p.ID)
        if plate >= N_files:
            continue

        los = 'los_' + p.ID

        DD_MM = MODEL[los]['DD/MM']
        sig2  = ( DD_MM ** 2 ) * MODEL[los]['err2_temp']

        for i in range(len(DD_MM)):

            if DD_MM[i] <= 0.0 or sig2[i] <= 0.0:
                continue

            chi2 += (DD_MM[i] - 1)**2 * (sig2[i] ** -1)

    return(chi2)


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
    N_std   = int(args_array[4])

    ####################_PARAMETERS_########################


    ###################_INITIALIZATION_#####################

    # Blank dictionaries to be filled as follows:
    # MODEL (1 dict.): los (152 dict.): bin (12 dict.): ind1, ind2 (arrays); jk_err, DD/MM, err2_temp (floats)
        #ind1 and ind2 are pair indices for each bin in each los
    # DATA (1 dict.): los (152 dict.): bin (12 dict.): DD, jk_err (floats)
    # MODEL_ZRW (1 dict): los (152 dict.): norm (float); Z, R, W (arrays)

    MODEL    = {}
    DATA     = {}
    MODEL_ZR = {}

    # Arrays of parameter values for each mcmc step
    A       = np.zeros(N_loops)
    Z_THICK = np.zeros(N_loops)
    R_THICK = np.zeros(N_loops)
    Z_THIN  = np.zeros(N_loops)
    R_THIN  = np.zeros(N_loops)
    A[0], Z_THICK[0], R_THICK[0], Z_THIN[0], R_THIN[0] = assign_params(
        a, z_thick, r_thick, z_thin, r_thin, 0, N_std)

    CHI2      = np.zeros(N_loops)
    CHI2_TEST = np.zeros(N_loops)
    EFF       = np.zeros(N_loops)
    EFF[0]    = 0

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
        # DATA[los]     = {}
        MODEL_ZR[los] = {}

        # File containing ascii data for uniform samples (has Z and R; W is 1)
        ZR_file = jk_dir + 'uniform_' + p.ID + '.ascii.dat'

        MODEL_ZR[los]['Z'], MODEL_ZR[los]['R'], = np.genfromtxt(
            ZR_file, unpack=True, skiprows=1, usecols=[5, 6], dtype=None)

        # Load jackknife errors as numpy arrays: one error for each bin
        uni_jk_file             = jk_dir + 'uniform_' + p.ID + '_jk_error.dat'
        uni_jk_err              = np.genfromtxt(uni_jk_file, unpack=True, usecols=[7])
        dat_jk_file             = jk_dir + 'star_' + p.ID + '_jk_error.dat'
        dat_jk_err              = np.genfromtxt(dat_jk_file, unpack=True, usecols=[7])
        # MODEL[los]['err2_temp'] = uni_jk_err ** 2 + dat_jk_err ** 2
        #Multiply err2_temp by DD/MM **2 to get sigma2 in DD/MM

        err2_temp = np.zeros(len(dat_jk_err))

        for i in range(len(err2_temp)):
            if uni_jk_err[i] == 0.0 or dat_jk_err[i] == 0.0:
                continue
            err2_temp[i] = uni_jk_err[i] ** 2 + dat_jk_err[i] ** 2

        MODEL[los]['err2_temp'] = err2_temp

        # Load normalized and weighted DD counts
        DD_file         = DD_dir + 'DD_' + p.ID + '.dat'
        MODEL[los]['DD'] = np.genfromtxt(DD_file, usecols=[2])


        for j in range(Nbins):

            BIN             = 'bin_' + str(j)

            MODEL[los][BIN] = {}

            model_file      = uni_pairs_dir + 'counts_' + p.ID + '.bin_' + str(j + 1) + '.dat'

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

        weight = ( ( ( np.cosh(MODEL_ZR[los]['Z'] * ( 2 * Z_THIN[0] ) ** (-1) ) ) ** (-2) )
            * np.exp(-MODEL_ZR[los]['R'] * (R_THIN[0] ** -1)) +
            A[0] * ( ( np.cosh(MODEL_ZR[los]['Z'] * (2 * Z_THICK[0]) ** (-1) ) ) ** (-2) )
            * np.exp(-MODEL_ZR[los]['R'] * R_THICK[0] ** -1) )

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

        MODEL[los]['DD/MM'] = DD_MM


    print('Number of degrees of freedom: ', N_dof, '\n')
    # Calculate initial chi2

    CHI2[0]      = chi2(todo_list, N_files, MODEL)
    CHI2_TEST[0] = CHI2[0]

    #################_MODEL_INITIALIZATION_#################


    ########################_MCMC_##########################

    k = 1   # start loop index at 1 because of initialization

    while k < (N_loops):

        print('Loop number: ', k)

        # Assign new params
        A[k], Z_THICK[k], R_THICK[k], Z_THIN[k], R_THIN[k] = assign_params(
            A[k-1], Z_THICK[k-1], R_THICK[k-1], Z_THIN[k-1], R_THIN[k-1])

        for p in todo_list:

            plate = int(p.ID)
            if plate >= N_files:
                continue

            los = 'los_' + p.ID

            weight = ( ( ( np.cosh(MODEL_ZR[los]['Z'] * ( 2 * Z_THIN[k] ) ** (-1) ) ) ** (-2) )
                * np.exp(-MODEL_ZR[los]['R'] * (R_THIN[k] ** -1)) +
                A[k] * ( ( np.cosh(MODEL_ZR[los]['Z'] * (2 * Z_THICK[k]) ** (-1) ) ) ** (-2) )
                * np.exp(-MODEL_ZR[los]['R'] * R_THICK[k] ** -1) )

            # MODEL_ZRW[los]['norm'] = norm_weights(MODEL_ZRW[los]['W'])
            norm = ( np.sum(weight) ** 2 - np.inner(weight, weight) ) / 2

            MM_temp = np.zeros(Nbins)
            DD      = MODEL[los]['DD']
            DD_MM   = np.ones(Nbins)   # Set as 1 to start. If DD/MM = 1, then no contribution to chi2.

            # This should maybe be replaced with list comprehension if possible
            for j in range(Nbins):

                BIN = 'bin_' + str(j)

                if DD[j] > 0:

                    MM_temp[j] = np.sum( weight[MODEL[los][BIN]['ind1']] *
                        weight[MODEL[los][BIN]['ind2']] ) * (norm ** -1)

                    if MM_temp[j] <=0:
                        continue
                    else:
                        DD_MM[j] = DD[j] / MM_temp[j]


            MODEL[los]['DD/MM'] = DD_MM


        CHI2[k]    = chi2(todo_list, N_files, MODEL)
        CHI2_TEST[k] = CHI2[k]

        delta_chi2 = CHI2[k] - CHI2[k - 1]


        if delta_chi2 < 0:

            N_acc += 1

        else:

            rnd = random.random()

            test = math.exp(-delta_chi2 / 2)

            if rnd < test:

                N_acc += 1

            else:

                CHI2[k]    = CHI2[k-1]
                A[k]       = A[k-1]
                Z_THICK[k] = Z_THICK[k-1]
                Z_THIN[k]  = Z_THIN[k-1]
                R_THICK[k] = R_THICK[k-1]
                R_THIN[k]  = R_THIN[k-1]

        EFF[k] = N_acc / k
        k += 1

    np.savez(outfile, CHI2=CHI2, CHI2_TEST=CHI2_TEST, EFF=EFF, A=A, Z_THICK=Z_THICK,
        Z_THIN=Z_THIN, R_THICK=R_THICK, R_THIN=R_THIN)

    print('MCMC done. Data output to: ', outfile)

if __name__ == '__main__':
    main()
