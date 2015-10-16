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

@profile

def gal_weights(Z, R, z_thick, r_thick, z_thin, r_thin, a):

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

@profile
def norm_weights(w):

    '''
    For an array of weights, calculates the normalization
    factor.
    '''

    norm = 0

    for i in range(len(w)):

        for j in range(i + 1, len(w)):

            norm += w[i] * w[j]

    return norm

#############################################################
@profile
def assign_params(a, z_thc, z_thn, r_thc, r_thn):


    # std of step size for each: should this be variable?
    a_std     = 0.005
    z_thc_std = 0.016
    z_thn_std = 0.007
    r_thc_std = 0.19
    r_thn_std = 0.48
    a         = np.random.normal(a, a_std)
    z_thc     = np.random.normal(z_thc, z_thc_std)
    z_thn     = np.random.normal(z_thn, z_thn_std)
    r_thc     = np.random.normal(r_thc, r_thc_std)
    r_thn     = np.random.normal(r_thn, r_thn_std)

    return(a, z_thc, z_thn, r_thc, r_thn)

@profile
def main():

    np.random.seed()

    # Set mcmc loop parameters
    N_mcmc = 10
    mc_eff = 0
    N_params = 5
    params = np.zeros((N_mcmc, N_params))

    '''Describe these dictionaries somewhere.'''
    MODEL     = {}
    DATA      = {}
    MODEL_ZRW = {}

    # Read in various pointings
    input_filename = rawdata_dir + 'todo_list.dat'
    # sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    N_los = len(todo_list)

    N_files = 5   #Number of files I feel like testing


    # Loading pair indices, data file,
    for p in todo_list:

        plate = int(p.ID)
        if plate >= N_files:
            continue

        # print('Loading pair:', p.ID, time.time() - start, '\n')
        print('Pair:', p.ID)

        los         = 'los_' + p.ID
        MODEL[los]  = {}
        DATA[los]   = {}
        MODEL_ZRW[los] = {}

        # File containing ascii data for uniform samples (has Z and R)
        ZRW_file = jk_dir + 'uniform_' + p.ID + '.ascii.dat'

        MODEL_ZRW[los]['Z'], MODEL_ZRW[los]['R'], MODEL_ZRW[los]['W'] = np.genfromtxt(
            ZRW_file, unpack=True, skiprows=1, usecols=[5, 6, 10])

        MODEL_ZRW[los]['norm'] = 1              #This will change

        uni_jk_file = jk_dir + 'uniform_' + p.ID + '_jk_error.dat'
        uni_jk_err  = np.genfromtxt(uni_jk_file, unpack=True, usecols=[7])

        dat_jk_file = jk_dir + 'star_' + p.ID + '_jk_error.dat'
        dat_jk_err  = np.genfromtxt(dat_jk_file, unpack=True, usecols=[7])

        DD_file     = DD_dir + 'DD_' + p.ID + '.dat'
        DD          = np.genfromtxt(DD_file, usecols=[2])   #weighted and normalized


        for j in range(Nbins):

            bin = 'bin_' + str(j)

            MODEL[los][bin] = {}
            DATA[los][bin]  = {}

            model_file      = uni_pairs_dir + 'counts_' + p.ID + '.bin_' + str(j + 1) + '.dat'

            MODEL[los][bin]['ind1'], MODEL[los][bin]['ind2'] = np.genfromtxt(
                model_file, dtype=None, unpack=True)

            MODEL[los][bin]['jk_err']    = uni_jk_err[j]

            # input DD counts here:
            DATA[los][bin]['DD']         = DD[j]

            DATA[los][bin]['jk_err']     = dat_jk_err[j]

            MODEL[los][bin]['DD/MM']     = 0

            # Might as well just calculate sig2 squared bc it'll be used
            # later in finding chi2
            MODEL[los][bin]['sigma2_jk'] = (MODEL[los][bin]['jk_err'] ** 2
                + DATA[los][bin]['jk_err'] ** 2)

    # Set initial parameters
    a_std     = 0.005
    z_thc_std = 0.016
    z_thn_std = 0.007
    r_thc_std = 0.19
    r_thn_std = 0.48

    z_thick = 0.674 + 5 * z_thc_std
    r_thick = 2.51 + 5 * r_thc_std
    z_thin  = 0.233 + 5 * z_thn_std
    r_thin  = 2.34 + 5 * r_thn_std
    a       = 0.12

    count = 0


    # Weight model points and calculate DD/MM
    # print('Int. weights:', time.time() - start, '\n')
    for i in range(N_files):
    # for p in todo_list:

        # i = p.ID

        los = 'los_' + str(i)

        MODEL_ZRW[los]['W'] = gal_weights(MODEL_ZRW[los]['Z'], MODEL_ZRW[los]['R'],
            z_thick, r_thick, z_thin, r_thin, a)


        MODEL_ZRW[los]['norm'] = norm_weights(MODEL_ZRW[los]['W'])

        # print(i)

        for j in range(Nbins):

            bin = 'bin_' + str(j)

            # This line looks like a mess, but it's really just the sum of all the multiples
            # of weights of pairs. Even that sentence was a bit confusing.

            MODEL[los][bin]['MM'] = np.sum( MODEL_ZRW[los]['W'][MODEL[los][bin]['ind1']] *
                MODEL_ZRW[los]['W'][MODEL[los][bin]['ind2']] )

            MODEL[los][bin]['MM'] /= MODEL_ZRW[los]['norm']

            # I could probably move this next line to earlier in the code to skip doing anything
            # for los with 0 data counts.

            if DATA[los][bin]['DD'] <= 0 or MODEL[los][bin]['MM'] <= 0:
                # count += 1
                continue

            MODEL[los][bin]['DD/MM'] = DATA[los][bin]['DD'] / MODEL[los][bin]['MM']

    # print(count)


    # # # Calculate initial chi2
    chi2 = 0

    # # I should include a line to count D.O.F.
    for i in range(N_files):
    # for p in todo_list:

        # i = p.ID

        los = 'los_' + str(i)

        for j in range(Nbins):

            bin = 'bin_' + str(j)

            if MODEL[los][bin]['DD/MM'] <= 0:
                continue

            # Son of a bitch this is wrong.

            sig2 = MODEL[los][bin]['DD/MM'] * MODEL[los][bin]['sigma2_jk']

            chi2 += ((MODEL[los][bin]['DD/MM'] - 1) ** 2) / sig2







    # Now do loop:

    # Take random walk in parameter space

    # Set new weights with new parameters and
    # do new model pair counting

    # Calculate chi2

    # Accept/Reject, add values to params

    np.random.seed()

    N_loops = 20
    accept_rate = 0
    k = 1   #Start counter at 1 because we already did the inital value

    A, Z_THC, R_THC, Z_THN, R_THN = np.zeros(N_loops + 1), np.zeros(N_loops + 1), np.zeros(N_loops + 1), np.zeros(N_loops + 1), np.zeros(N_loops + 1)

    A[0], Z_THC[0], R_THC[0], Z_THN[0], R_THN[0] = a, z_thick, r_thick, z_thin, r_thin

    CHI2 = np.zeros(N_loops + 1)
    CHI2[0] = chi2

    # print('Starting mcmc:', time.time() - start, '\n')


    while k < (N_loops + 1):

        print('Loop number:', k)

        '''Assign new params'''
        a, z_thc, z_thn, r_thc, r_thn = assign_params(A[k-1], Z_THC[k-1], Z_THN[k-1], R_THC[k-1], R_THN[k-1])

        '''Assign new weights and calc. DD/MM'''
        for i in range(N_files):

        # for p in todo_list:

            # i = p.ID

            los = 'los_' + str(i)

            MODEL_ZRW[los]['W'] = gal_weights(MODEL_ZRW[los]['Z'], MODEL_ZRW[los]['R'],
                z_thick, r_thick, z_thin, r_thin, a)


            MODEL_ZRW[los]['norm'] = norm_weights(MODEL_ZRW[los]['W'])

            # print(i)

            for j in range(Nbins):

                bin = 'bin_' + str(j)

                # This line looks like a mess, but it's really just the sum of all the multiples
                # of weights of pairs. Even that sentence was a bit confusing.

                MODEL[los][bin]['MM'] = np.sum( MODEL_ZRW[los]['W'][MODEL[los][bin]['ind1']] *
                    MODEL_ZRW[los]['W'][MODEL[los][bin]['ind2']] )

                MODEL[los][bin]['MM'] /= MODEL_ZRW[los]['norm']

                # I could probably move this next line to earlier in the code to skip doing anything
                # for los with 0 data counts.

                if DATA[los][bin]['DD'] <= 0 or MODEL[los][bin]['MM'] <= 0:
                    # count += 1
                    continue

                MODEL[los][bin]['DD/MM'] = DATA[los][bin]['DD'] / MODEL[los][bin]['MM']


        '''Calculate chi-squared'''

        chi2 = 0

        for i in range(N_files):

        # for p in todo_list:

        #     i = p.ID

            los = 'los_' + str(i)

            for j in range(Nbins):

                bin = 'bin_' + str(j)

                if MODEL[los][bin]['DD/MM'] <= 0:
                    continue

                # chi2 += MODEL[los][bin]['DD/MM'] * MODEL[los][bin]['sigma2_jk']
                sig2 = MODEL[los][bin]['DD/MM'] * MODEL[los][bin]['sigma2_jk']

                chi2 += ((MODEL[los][bin]['DD/MM'] - 1) ** 2) / sig2

        delta_chi2 = chi2 - CHI2[k - 1]

        if delta_chi2 < 0:

            CHI2[k] = chi2
            A[k], Z_THC[k], Z_THN[k], R_THC[k], R_THN[k] = a, z_thc, z_thn, r_thc, r_thn
            accept_rate += 1

        else:

            rnd = random.random()

            test = math.exp(-delta_chi2 / 2)

            if rnd < test:  #Why less than?

                CHI2[k] = chi2
                A[k], Z_THC[k], Z_THN[k], R_THC[k], R_THN[k] = a, z_thc, z_thn, r_thc, r_thn
                accept_rate += 1

            else:

                CHI2[k] = CHI2[k - 1]

                A[k], Z_THC[k], Z_THN[k], R_THC[k], R_THN[k] = A[k-1], Z_THC[k-1], Z_THN[k-1], R_THC[k-1], R_THN[k-1]

        k += 1


    print('Accept Rate:', accept_rate / N_loops)
    # print(A, Z_THC, Z_THN, R_THC, R_THN)

    np.savetxt('A.dat', A)
    np.savetxt('Z_THC.dat', Z_THC)
    np.savetxt('Z_THN.dat', Z_THN)
    np.savetxt('R_THC.dat', R_THC)
    np.savetxt('R_THN.dat', R_THN)

if __name__ == '__main__':
    main()