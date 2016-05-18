import config
import math, pickle

def main():
    '''Make a set of distance bins, and output in different format.
    These will be used for error calculation and mcmc.
    '''
    # set the initials from config.py
    r_min = config.R_min
    r_max = config.R_max
    N = config.N_rbins

    # make log bins
    r_min_log = math.log10(r_min)
    r_max_log = math.log10(r_max)
    dr_log = (r_max_log - r_min_log) / N

    bins_list = []

    for i in range(N):
        b = config.R_Bin()

        b.r_lower_log = r_min_log + dr_log * i
        b.r_upper_log = b.r_lower_log + dr_log
        b.r_middle_log = b.r_lower_log + 0.5 * dr_log

        b.r_lower = 10.0**b.r_lower_log
        b.r_upper = 10.0**b.r_upper_log
        b.r_middle = 10.0**b.r_middle_log
        b.dr = b.r_upper - b.r_lower

        bins_list.append(b)

    # pickle output
    output_filename = config.data_dir + 'rbins.dat'
    output_file     = open(output_filename, 'wb')
    pickle.dump(bins_list, output_file)
    output_file.close()

    # ascii output
    output_filename = config.data_dir + 'rbins.ascii.dat'
    output_file = open(output_filename, 'w')
    # output number of bins first
    output_file.write('{}\n'.format(len(bins_list)))
    for b in bins_list:
        output_file.write('{}\t{}\t{}\t{}\n'
                          .format(b.r_lower, b.r_upper, b.r_middle, b.dr))
    output_file.close()

    sys.stderr.write('Bins list output to {}\n\n'.format(config.data_dir))


if __name__ == '__main__':
    main()

