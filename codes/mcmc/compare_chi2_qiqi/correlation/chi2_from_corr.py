from config import *

'''
Load the file containing Qingqing's values for each step in his mcmc
chain. For each set of his params, use my code to calculate the value
of chi2 and compare.
'''


#############################################################

# @profile
def chi2(todo_list, MODEL):

    '''Calculates chi-square for given model'''

    chi2 = 0

    for p in todo_list:

        los = 'los_' + p.ID

        corr = MODEL[los]['corr']
        DD_MM = corr + 1
        sig2  = ( DD_MM ** 2 ) * MODEL[los]['err2_temp']

        for i in range(len(DD_MM)):

            if DD_MM[i] <= 0.0:
                continue

            chi2 += (DD_MM[i] - 1)**2 * (sig2[i] ** -1)

    return(chi2)


#############################################################

#############################################################

# @profile
def main():



    ####################_PARAMETERS_########################


    ###################_INITIALIZATION_#####################

    # Blank dictionaries to be filled as follows:
    # MODEL (1 dict.): los (152 dict.): bin (12 dict.): ind1, ind2 (arrays); jk_err, DD/MM, err2_temp (floats)
        #ind1 and ind2 are pair indices for each bin in each los
    # DATA (1 dict.): los (152 dict.): bin (12 dict.): DD, jk_err (floats)
    # MODEL_ZRW (1 dict): los (152 dict.): norm (float); Z, R, W (arrays)

    MODEL = {}

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
        los = 'los_' + p.ID
        print(los)

        # Subdictionaries for each los
        los           = 'los_' + p.ID
        MODEL[los]    = {}

        # Load jackknife errors as numpy arrays: one error for each bin
        uni_jk_file             = qiqi_dir + 'uniform_' + p.ID + '_jk_error.dat'
        uni_jk_err              = np.genfromtxt(uni_jk_file, unpack=True, usecols=[7])
        dat_jk_file             = qiqi_dir + 'star_' + p.ID + '_jk_error.dat'
        dat_jk_err              = np.genfromtxt(dat_jk_file, unpack=True, usecols=[7])
        MODEL[los]['err2_temp'] = uni_jk_err ** 2 + dat_jk_err ** 2
        #Multiply err2_temp by DD/MM **2 to get sigma2 in DD/MM

        # Load normalized and weighted DD counts
        corr_file          = corr_dir + 'correlation_' + p.ID + '.dat'
        MODEL[los]['corr'] = np.genfromtxt(corr_file, usecols=[1])

        CHI2               = chi2(todo_list, MODEL)

    print('Chi-squared is: ', CHI2)

if __name__ == '__main__':
    main()
