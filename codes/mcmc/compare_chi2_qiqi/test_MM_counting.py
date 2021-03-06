from config import *

'''
Compare the value of MM obtained from calcualtions within my code
to MM obtained from direct pair counting.
'''


# @profile
def main():

    elements_needed = int(3)
    args_array      = np.array(sys.argv)
    N_args          = len(args_array)
    assert(N_args   == elements_needed)
    infile          = args_array[1]
    infile          = chi2min_dir + infile
    outfile         = args_array[2]
    outfile         = out_dir + outfile

    chi2_qiqi, r_thin, z_thin, r_thick, z_thick, a = np.genfromtxt(infile, unpack=True)

    print("Expected minimum chi2 is ", chi2_qiqi)

    MODEL    = {}
    MODEL_ZR = {}

    # Lines of sight

    input_filename = rawdata_dir + 'todo_list.dat'
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()
    N_los          = len(todo_list)

    MM_CORR = []
    MM_MCMC = []
    LOS_NUM = []
    BIN_NUM = []

    r_thin  = 2.02695
    z_thin  = 0.233619
    r_thick = 2.3965745
    z_thick = 0.674525
    a       = 0.052944

    # Loading data into dictionaries and subdictionaries
    for p in todo_list:

        print('Loading Pointing #', p.ID)

        # Subdictionaries for each los
        los           = 'los_' + p.ID
        MODEL[los]    = {}
        MODEL_ZR[los] = {}

        # File containing ascii data for uniform samples (has Z and R; W is 1)
        ZR_file = qiqi_dir + 'uniform_' + p.ID + '.ascii.dat'

        MODEL_ZR[los]['Z'], MODEL_ZR[los]['R'], = np.genfromtxt(
            ZR_file, unpack=True, skip_header=1, usecols=[5, 6], dtype=None)

        weight = ( ( ( np.cosh(MODEL_ZR[los]['Z'] * ( 2 * z_thin ) ** (-1) ) ) ** (-2) )
            * np.exp(-MODEL_ZR[los]['R'] * (r_thin ** -1)) +
            a * ( ( np.cosh(MODEL_ZR[los]['Z'] * (2 * z_thick) ** (-1) ) ) ** (-2) )
            * np.exp(-MODEL_ZR[los]['R'] * r_thick ** -1) )

        norm    = ( np.sum(weight) ** 2 - np.inner(weight, weight) ) / 2
        MM_temp = np.zeros(Nbins)

        MM_file = weighted_dir + 'MM_' + p.ID + '.dat'
        MODEL[los]['MM_corr'] = np.genfromtxt(MM_file, unpack=True, usecols=[2])


        for j in range(Nbins):

            BIN             = 'bin_' + str(j)

            MODEL[los][BIN] = {}

            model_file      = model_dir + 'counts_' + p.ID + '.bin_' + str(j + 1) + '.dat'

            MODEL[los][BIN]['ind1'], MODEL[los][BIN]['ind2'] = np.genfromtxt(
                model_file, dtype=None, unpack=True)

            MM_temp[j] = np.sum( weight[MODEL[los][BIN]['ind1']] *
                weight[MODEL[los][BIN]['ind2']] ) * (norm ** -1)

        MODEL[los]['MM_mcmc'] = MM_temp

        for j in range(Nbins):

            MM_CORR.append(MODEL[los]['MM_corr'][j])
            MM_MCMC.append(MODEL[los]['MM_mcmc'][j])
            LOS_NUM.append(int(p.ID))
            BIN_NUM.append(j)


    MM_CORR = np.asarray(MM_CORR)
    MM_MCMC = np.asarray(MM_MCMC)
    LOS_NUM = np.asarray(LOS_NUM)
    BIN_NUM = np.asarray(BIN_NUM)

    temp1   = np.column_stack((MM_CORR, MM_MCMC))
    temp2   = np.column_stack((LOS_NUM, BIN_NUM))
    result  = np.column_stack((temp1, temp2))

    np.savetxt(outfile, result)


if __name__ == '__main__':
    main()
