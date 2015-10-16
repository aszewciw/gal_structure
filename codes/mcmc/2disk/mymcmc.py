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
def gal_weights(Z, R, a, z_thick, r_thick, z_thin, r_thin):

    '''
    For numpy arrays of (Z,R) values of different star,
    calculates the "weight" of each star based on the 5
    parameters.
    '''

    weight = ( ( ( np.cosh(Z / 2 / z_thin) ) ** (-2) )
        * np.exp(-R / r_thin) +
        a * ( ( np.cosh(Z / 2 / z_thick) ) ** (-2) )
        * np.exp(-R / r_thick))

    return weight

#############################################################


#############################################################

# @profile
def norm_weights(w):

    '''
    For an array of weights, calculates the normalization
    factor.
    '''

    norm = ( np.sum(w) ** 2 - np.inner(w,w)) / 2

    return norm

#############################################################

#############################################################

# @profile
def assign_params(a, z_thick, r_thick, z_thin, r_thin, init=1):

    '''
    Assigns new parameters based on current values
    and "known" standard deviation from Mao et. al.
    init will have value 0 if we are initializing
    values.
    '''
    a_std     = 0.005
    z_thick_std = 0.016
    r_thick_std = 0.19
    z_thin_std = 0.007
    r_thin_std = 0.48

    if init == 0:

        a       += N_std * a_std
        z_thick += N_std * z_thick_std
        r_thick += N_std * r_thick_std
        z_thin  += N_std * z_thin_std
        r_thin  += N_std * r_thin_std

    else:

        a     = np.random.normal(a, a_std)
        z_thick = np.random.normal(z_thick, z_thick_std)
        r_thick = np.random.normal(r_thick, r_thick_std)
        z_thin = np.random.normal(z_thin, z_thin_std)
        r_thin = np.random.normal(r_thin, r_thin_std)

    return(a, z_thick, r_thick, z_thin, r_thin)

#############################################################

#############################################################

# @profile
def chi2(todo_list, N_files, MODEL):

    '''Calculates chi-square for given model'''

    chi2 = 0

    for p in todo_list:

        plate = int(p.ID)
        if plate >= N_files:
            continue

        los = 'los_' + p.ID

        for j in range(Nbins):

            bin = 'bin_' + str(j)

            if MODEL[los][bin]['DD/MM'] <= 0:
                continue

            sig2 = ( MODEL[los][bin]['DD/MM'] ** 2 ) * MODEL[los][bin]['err2_temp']

            chi2 += ((MODEL[los][bin]['DD/MM'] - 1) ** 2) / sig2

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

    N_loops  = int(input('Enter number of mcmc loops: '))   # Number of mcmc loops
    N_files  = int(input('Enter maximum number of files to test: '))        # should probably fix this so it prompts until you give an int

    ####################_PARAMETERS_########################


    ###################_INITIALIZATION_#####################

    # Blank dictionaries to be filled as follows:
    # MODEL (1 dict.): los (152 dict.): bin (12 dict.): ind1, ind2 (arrays); jk_err, DD/MM, err2_temp (floats)
        #ind1 and ind2 are pair indices for each bin in each los
    # DATA (1 dict.): los (152 dict.): bin (12 dict.): DD, jk_err (floats)
    # MODEL_ZRW (1 dict): los (152 dict.): norm (float); Z, R, W (arrays)

    MODEL     = {}
    DATA      = {}
    MODEL_ZRW = {}

    # Arrays of parameter values for each mcmc step
    A, Z_THICK, R_THICK, Z_THIN, R_THIN = np.zeros(N_loops), np.zeros(N_loops), np.zeros(N_loops), np.zeros(N_loops), np.zeros(N_loops)
    A[0], Z_THICK[0], R_THICK[0], Z_THIN[0], R_THIN[0] = assign_params(a, z_thick, r_thick, z_thin, r_thin, 0)

    CHI2 = np.zeros(N_loops)

    ###################_INITIALIZATION_#####################


    ####################_DATA_INPUT_########################

    # Lines of sight

    input_filename = rawdata_dir + 'todo_list.dat'
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()
    N_los = len(todo_list)


    # Loading data into dictionaries and subdictionaries
    for p in todo_list:

        # Limit number of los
        plate = int(p.ID)
        if plate >= N_files:
            continue

        print('Loading Pointing #', p.ID)

        # Subdictionaries for each los
        los            = 'los_' + p.ID
        MODEL[los]     = {}
        DATA[los]      = {}
        MODEL_ZRW[los] = {}

        # File containing ascii data for uniform samples (has Z and R; W is 1)
        ZRW_file = jk_dir + 'uniform_' + p.ID + '.ascii.dat'
        MODEL_ZRW[los]['Z'], MODEL_ZRW[los]['R'], MODEL_ZRW[los]['W'] = np.genfromtxt(
            ZRW_file, unpack=True, skiprows=1, usecols=[5, 6, 10])

        # Load jackknife errors as numpy arrays: one error for each bin
        uni_jk_file = jk_dir + 'uniform_' + p.ID + '_jk_error.dat'
        uni_jk_err  = np.genfromtxt(uni_jk_file, unpack=True, usecols=[7])
        dat_jk_file = jk_dir + 'star_' + p.ID + '_jk_error.dat'
        dat_jk_err  = np.genfromtxt(dat_jk_file, unpack=True, usecols=[7])
        err2_temp   = uni_jk_err ** 2 + dat_jk_err ** 2         #Multiply this by DD/MM **2 to get error2 in DD/MM

        # Load normalized and weighted DD counts
        DD_file     = DD_dir + 'DD_' + p.ID + '.dat'
        DD          = np.genfromtxt(DD_file, usecols=[2])


        for j in range(Nbins):

            bin = 'bin_' + str(j)

            MODEL[los][bin] = {}
            DATA[los][bin]  = {}

            model_file      = uni_pairs_dir + 'counts_' + p.ID + '.bin_' + str(j + 1) + '.dat'

            MODEL[los][bin]['ind1'], MODEL[los][bin]['ind2'] = np.genfromtxt(
                model_file, dtype=None, unpack=True)

            # input DD counts here:
            DATA[los][bin]['DD'] = DD[j]

            #We want to skip any los with DD = 0 (also with MM = 0, but these don't exist)
            if DATA[los][bin]['DD'] == 0:

                # We won't count these when calculating chi2
                MODEL[los][bin]['err2_temp'] = 0

            else:

                MODEL[los][bin]['err2_temp'] = err2_temp[j]

    ####################_DATA_INPUT_########################



    #################_MODEL_INITIALIZATION_#################

    # Weight model points and calculate DD/MM

    for p in todo_list:

        plate = int(p.ID)
        if plate >= N_files:
            continue

        los = 'los_' + p.ID

        MODEL_ZRW[los]['W'] = gal_weights(MODEL_ZRW[los]['Z'], MODEL_ZRW[los]['R'],
            A[0], Z_THICK[0], R_THICK[0], Z_THIN[0], R_THIN[0])

        MODEL_ZRW[los]['norm'] = norm_weights(MODEL_ZRW[los]['W'])

        for j in range(Nbins):

            bin = 'bin_' + str(j)

            # normalized sum of product of weights for each pair
            MODEL[los][bin]['MM'] = np.sum( MODEL_ZRW[los]['W'][MODEL[los][bin]['ind1']] *
                MODEL_ZRW[los]['W'][MODEL[los][bin]['ind2']] ) / MODEL_ZRW[los]['norm']


            # Skip any pairs with 0 DD or MM
            if DATA[los][bin]['DD'] <= 0 or MODEL[los][bin]['MM'] <= 0:

                MODEL[los][bin]['DD/MM'] = 0

            else:

                MODEL[los][bin]['DD/MM'] = DATA[los][bin]['DD'] / MODEL[los][bin]['MM']

                N_dof += 1


    # Calculate initial chi2

    CHI2[0] = chi2(todo_list, N_files, MODEL)

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

            MODEL_ZRW[los]['W'] = gal_weights(MODEL_ZRW[los]['Z'], MODEL_ZRW[los]['R'],
                A[k], Z_THICK[k], R_THICK[k], Z_THIN[k], R_THIN[k])


            MODEL_ZRW[los]['norm'] = norm_weights(MODEL_ZRW[los]['W'])

            for j in range(Nbins):

                bin = 'bin_' + str(j)

                # normalized sum of product of weights for each pair
                MODEL[los][bin]['MM'] = np.sum( MODEL_ZRW[los]['W'][MODEL[los][bin]['ind1']] *
                    MODEL_ZRW[los]['W'][MODEL[los][bin]['ind2']] ) / MODEL_ZRW[los]['norm']

                # I could probably move this next line to earlier in the code to skip doing anything
                # for los with 0 data counts.

                MODEL[los][bin]['DD/MM'] = DATA[los][bin]['DD'] / MODEL[los][bin]['MM']

                if DATA[los][bin]['DD'] <= 0 or MODEL[los][bin]['MM'] <= 0:

                    MODEL[los][bin]['DD/MM'] = 0

                else:

                    MODEL[los][bin]['DD/MM'] = DATA[los][bin]['DD'] / MODEL[los][bin]['MM']


        CHI2[k] = chi2(todo_list, N_files, MODEL)

        delta_chi2 = CHI2[k] - CHI2[k - 1]


        if delta_chi2 < 0:

            N_acc += 1

        else:

            rnd = random.random()

            test = math.exp(-delta_chi2 / 2)

            if rnd < test:  #Why less than?

                N_acc += 1

            else:

                CHI2[k], A[k], Z_THICK[k], R_THICK[k], Z_THIN[k], R_THIN[k] = CHI2[k - 1], A[k-1], Z_THICK[k-1], R_THICK[k-1], Z_THIN[k-1], R_THIN[k-1]

        k += 1


    # print('Accept Rate:', accept_rate / N_loops)
    # print(A, Z_THC, Z_THN, R_THC, R_THN)

    np.savetxt('A.dat', A)
    np.savetxt('Z_THICK.dat', Z_THICK)
    np.savetxt('Z_THIN.dat', Z_THIN)
    np.savetxt('R_THICK.dat', R_THICK)
    np.savetxt('R_THIN.dat', R_THIN)

if __name__ == '__main__':
    main()