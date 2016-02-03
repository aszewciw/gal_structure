from config import *

'''
Check the difference between these two methods for calculating
the correlation function:
1. First weighting the model, then calculating DD/MM.
2. First binning the pair indices, then weighting the model,
then calculating DD/MM.
'''

#############################################################

def chi2(todo_list, MODEL):

    '''Calculates chi-square for given model'''

    chi2 = 0

    for p in todo_list:

        plate = int(p.ID)

        los   = 'los_' + p.ID

        DD_MM = MODEL[los]['DD/MM']
        sig2  = ( DD_MM ** 2 ) * MODEL[los]['err2_temp']
        chi2  += np.sum( ( ( DD_MM - 1 )**2 ) * ( sig2 ** -1 ) )

    return(chi2)


#############################################################

#############################################################

def main():

    np.random.seed()

    ####################_PARAMETERS_########################

    elements_needed = int(5)

    args_array    = np.array(sys.argv)
    N_args        = len(args_array)
    assert(N_args == elements_needed)
    outfile       = args_array[1]


    MODEL    = {}
    DATA     = {}
    MODEL_ZR = {}


    input_filename = rawdata_dir + 'todo_list.dat'
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()
    N_los          = len(todo_list)


    # Loading data into dictionaries and subdictionaries
    for p in todo_list:

        # Limit number of los
        plate = int(p.ID)

        print('Loading Pointing #', p.ID)

        # Subdictionaries for each los
        los           = 'los_' + p.ID
        MODEL[los]    = {}
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
        MODEL[los]['err2_temp'] = uni_jk_err ** 2 + dat_jk_err ** 2
        #Multiply err2_temp by DD/MM **2 to get sigma2 in DD/MM

        # Load normalized and weighted DD counts
        DD_file          = DD_dir + 'DD_' + p.ID + '.dat'
        MODEL[los]['DD'] = np.genfromtxt(DD_file, usecols=[2])


        for j in range(Nbins):

            BIN             = 'bin_' + str(j)

            MODEL[los][BIN] = {}

            model_file      = uni_pairs_dir + 'counts_' + p.ID + '.bin_' + str(j + 1) + '.dat'

            MODEL[los][BIN]['ind1'], MODEL[los][BIN]['ind2'] = np.genfromtxt(
                model_file, dtype=None, unpack=True)


    for p in todo_list:

        plate = int(p.ID)

        los = 'los_' + p.ID

        weight = ( ( ( np.cosh(MODEL_ZR[los]['Z'] * ( 2 * z_thin ) ** (-1) ) ) ** (-2) )
            * np.exp(-MODEL_ZR[los]['R'] * (r_thin ** -1)) +
            a * ( ( np.cosh(MODEL_ZR[los]['Z'] * (2 * z_thick) ** (-1) ) ) ** (-2) )
            * np.exp(-MODEL_ZR[los]['R'] * r_thick ** -1) )

        norm = ( np.sum(weight) ** 2 - np.inner(weight, weight)) / 2

        MM_temp = np.zeros(Nbins)
        DD      = MODEL[los]['DD']
        DD_MM   = np.ones(Nbins)   # Set as 1 to start. If DD/MM = 1, then no contribution to chi2.

        for j in range(Nbins):

            BIN = 'bin_' + str(j)

            if DD[j] > 0:

                MM_temp[j] = np.sum( weight[MODEL[los][BIN]['ind1']] *
                    weight[MODEL[los][BIN]['ind2']] ) * (norm ** -1)

                if MM_temp[j] <= 0:
                    continue
                else:
                    DD_MM[j] = DD[j] / MM_temp[j]
                    N_dof    += 1


        MODEL[los]['DD/MM'] = DD_MM

        for j in range(len(DD_MM)):
            if DD_MM[i]==1:
                DD_MM[i] = 0

        outfile = test_dir + 'mcmc_correlation_' + p.ID + '.dat'
        np.savetxt(outfile, DD_MM)


    print('Number of degrees of freedom: ', N_dof, '\n')
    # Calculate initial chi2

    chi2 = chi2(todo_list, MODEL)
    print('Chi-squared is: ', chi2)

    #################_MODEL_INITIALIZATION_#################


    # print('MCMC done. Data output to: ', outfile)

if __name__ == '__main__':
    main()