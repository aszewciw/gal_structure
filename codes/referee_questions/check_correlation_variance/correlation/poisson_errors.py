from config import *

def get_error(DD, DD_N, RR, RR_N):

    DD_RR = np.zeros(len(DD))

    for i in range(len(DD)):

        if RR[i] == 0.0:
            continue

        DD_RR[i] = DD[i] / RR[i]

    DD_raw = DD*DD_N
    RR_raw = RR*RR_N

    DD_err = np.sqrt(DD_raw) / DD_N
    RR_err = np.sqrt(RR_raw) / RR_N

    error = np.zeros(len(DD))

    for i in range(len(error)):

        if DD[i]==0.0 or RR[i]==0.0:
            continue

        error[i] = np.sqrt( ( (DD_err[i]/DD[i])**2 + (RR_err[i]/RR[i])**2 )
            * (DD_RR)**2 )

    return error


def main():

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

        f1_DD, f1_DD_N, f1_RR, f1_RR_N = np.genfromtxt(corr_file1,
            unpack=True, usecols=[3, 4, 5, 6])
        f2_DD, f2_DD_N, f2_RR, f2_RR_N = np.genfromtxt(corr_file2,
            unpack=True, usecols=[3, 4, 5, 6])
        f3_DD, f3_DD_N, f3_RR, f3_RR_N = np.genfromtxt(corr_file3,
            unpack=True, usecols=[3, 4, 5, 6])
        f4_DD, f4_DD_N, f4_RR, f4_RR_N = np.genfromtxt(corr_file4,
            unpack=True, usecols=[3, 4, 5, 6])

        f1_err = get_error(f1_DD, f1_DD_N, f1_RR, f1_RR_N)
        f2_err = get_error(f2_DD, f2_DD_N, f2_RR, f2_RR_N)
        f3_err = get_error(f3_DD, f3_DD_N, f3_RR, f3_RR_N)
        f4_err = get_error(f4_DD, f4_DD_N, f4_RR, f4_RR_N)

        error_file1 = data_dir + 'error_full_10data_' + p.ID + '.dat'
        error_file2 = data_dir + 'error_full_10mock_' + p.ID + '.dat'
        error_file3 = data_dir + 'error_full_1500_' + p.ID + '.dat'
        error_file4 = data_dir + 'error_full_2000_' + p.ID + '.dat'

        np.savetxt(error_file1, f1_err)
        np.savetxt(error_file2, f2_err)
        np.savetxt(error_file3, f3_err)
        np.savetxt(error_file4, f4_err)

        corr_file1 = data_dir + 'corr_cut_10data_' + p.ID + '.dat'
        corr_file2 = data_dir + 'corr_cut_10mock_' + p.ID + '.dat'
        corr_file3 = data_dir + 'corr_cut_1500_' + p.ID + '.dat'
        corr_file4 = data_dir + 'corr_cut_2000_' + p.ID + '.dat'

        f1_DD, f1_DD_N, f1_RR, f1_RR_N = np.genfromtxt(corr_file1,
            unpack=True, usecols=[3, 4, 5, 6])
        f2_DD, f2_DD_N, f2_RR, f2_RR_N = np.genfromtxt(corr_file2,
            unpack=True, usecols=[3, 4, 5, 6])
        f3_DD, f3_DD_N, f3_RR, f3_RR_N = np.genfromtxt(corr_file3,
            unpack=True, usecols=[3, 4, 5, 6])
        f4_DD, f4_DD_N, f4_RR, f4_RR_N = np.genfromtxt(corr_file4,
            unpack=True, usecols=[3, 4, 5, 6])

        f1_err = get_error(f1_DD, f1_DD_N, f1_RR, f1_RR_N)
        f2_err = get_error(f2_DD, f2_DD_N, f2_RR, f2_RR_N)
        f3_err = get_error(f3_DD, f3_DD_N, f3_RR, f3_RR_N)
        f4_err = get_error(f4_DD, f4_DD_N, f4_RR, f4_RR_N)

        error_file1 = data_dir + 'error_cut_10data_' + p.ID + '.dat'
        error_file2 = data_dir + 'error_cut_10mock_' + p.ID + '.dat'
        error_file3 = data_dir + 'error_cut_1500_' + p.ID + '.dat'
        error_file4 = data_dir + 'error_cut_2000_' + p.ID + '.dat'

        np.savetxt(error_file1, f1_err)
        np.savetxt(error_file2, f2_err)
        np.savetxt(error_file3, f3_err)
        np.savetxt(error_file4, f4_err)


if __name__ == '__main__':
    main()