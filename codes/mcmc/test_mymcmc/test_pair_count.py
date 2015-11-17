from config import *
import matplotlib.pyplot as plt

'''
Test of whether my binning of pairs is flawed.
Steps:
1. Read in known mock sample and errors.
2. Read in files containing Z, R, for every random star.
3. Read in pair files for every bin and los.
4. Weight random sample with values of known mock.
5. Read in errors and calculate chi2.
6. Calculate correlation.
'''
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
        * np.exp(-R / r_thick) )

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
def chi2(todo_list, MODEL):

    '''Calculates chi-square for given model'''

    chi2 = 0

    for p in todo_list:

        los = 'los_' + p.ID

        for j in range(Nbins):

            bin = 'bin_' + str(j)

            if MODEL[los][bin]['DD/MM'] <= 0:
                continue

            sig2 = ( MODEL[los][bin]['DD/MM'] ** 2 ) * MODEL[los][bin]['err2_temp']

            chi2 += ((MODEL[los][bin]['DD/MM'] - 1) ** 2) / sig2

    return(chi2)


#############################################################

def main():

    np.random.seed()

    ####################_PARAMETERS_########################

    outfile  = str(input('Enter filename with .png extension: '))
    outfile  = out_dir + outfile
    binplt = np.zeros(Nbins)
    for i in range(Nbins):
        binplt[i] = bins[i]

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

        print('Loading Pointing #', p.ID)


        # Subdictionaries for each los
        los            = 'los_' + p.ID
        MODEL[los]     = {}
        DATA[los]      = {}
        MODEL_ZRW[los] = {}

        # File containing ascii data for uniform samples (has Z and R; W is 1)
        ZRW_file = uni_dir + 'uniform_' + p.ID + '.ascii.dat'
        MODEL_ZRW[los]['Z'], MODEL_ZRW[los]['R'], MODEL_ZRW[los]['W'] = np.genfromtxt(
            ZRW_file, unpack=True, skiprows=1, usecols=[5, 6, 10])

        # Load jackknife errors as numpy arrays: one error for each bin
        uni_jk_file = jk_dir + 'uniform_' + p.ID + '_jk_error.dat'
        uni_jk_err  = np.genfromtxt(uni_jk_file, unpack=True, usecols=[7])
        dat_jk_file = jk_dir + 'mock_' + p.ID + '_jk_error.dat'
        dat_jk_err  = np.genfromtxt(dat_jk_file, unpack=True, usecols=[7])
        err2_temp   = uni_jk_err ** 2 + dat_jk_err ** 2         #Multiply this by DD/MM **2 to get error2 in DD/MM

        # Load normalized and weighted DD counts
        DD_file     = mock_dir + 'DD_' + p.ID + '.dat'
        DD          = np.genfromtxt(DD_file, usecols=[2])


        for j in range(Nbins):

            bin             = 'bin_' + str(j)

            MODEL[los][bin] = {}
            DATA[los][bin]  = {}

            model_file      = uni_dir + 'counts_' + p.ID + '.bin_' + str(j + 1) + '.dat'

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

    fig = plt.figure(figsize = (10, 8))
    ax = fig.add_subplot(1,1,1, axisbg = 'white')
    ax.set_xlabel('r (kpc)')
    ax.set_ylabel(r'$\displaystyle\frac{DD}{MM}$(r) - 1')
    ax.set_title('Two-point Correlation of SEGUE G-Dwarfs')
    ax.set_xscale('log')
    ax.set_xticklabels(['0.01', '0.1', '1'])


    for p in todo_list:

        los = 'los_' + p.ID

        MODEL_ZRW[los]['W'] = gal_weights(MODEL_ZRW[los]['Z'], MODEL_ZRW[los]['R'],
            a, z_thick, r_thick, z_thin, r_thin)

        MODEL_ZRW[los]['norm'] = norm_weights(MODEL_ZRW[los]['W'])

        corr = np.zeros(Nbins)

        for j in range(Nbins):

            bin = 'bin_' + str(j)

            # normalized sum of product of weights for each pair
            MODEL[los][bin]['MM'] = np.sum( MODEL_ZRW[los]['W'][MODEL[los][bin]['ind1']] *
                MODEL_ZRW[los]['W'][MODEL[los][bin]['ind2']] ) / MODEL_ZRW[los]['norm']


            # Skip any pairs with 0 DD or MM
            if DATA[los][bin]['DD'] <= 0 or MODEL[los][bin]['MM'] <= 0:

                MODEL[los][bin]['DD/MM'] = 0
                MODEL[los][bin]['corr'] = 0

            else:

                MODEL[los][bin]['DD/MM'] = DATA[los][bin]['DD'] / MODEL[los][bin]['MM']
                corr[j] = MODEL[los][bin]['DD/MM'] - 1

        ax.plot(binplt, corr, '0.75')

    chi2 = chi2(todo_list, MODEL)

    print(chi2)
    plt.savefig(outfile)

if __name__ == '__main__':
    main()