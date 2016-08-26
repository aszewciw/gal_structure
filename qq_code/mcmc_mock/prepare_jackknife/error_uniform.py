#!/usr/bin/env python


import os, sys, math, pickle
import numpy
import config

def main():

    # load pointing list
    input_filename = config.todo_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file = open(input_filename, 'rb')
    todo_list = pickle.load(input_file)
    input_file.close()

    # load bin settings
    input_filename = config.bins_dir + 'rbins.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file = open(input_filename, 'rb')
    bins_list = pickle.load(input_file)
    input_file.close()
    if len(bins_list) != config.N_rbins:
        sys.stderr.write("Error: Inconsistent R bins. Check set_rbins and config. \n")
        sys.exit()

    bins_filename = config.jk_dir + 'rbins.ascii.dat'

    for p in todo_list:
        # counting pairs for the whole box
        data_filename = config.jk_dir + 'uniform_' + p.ID + '_jk_all.dat'
        counts_filename = config.jk_dir + 'uniform_' + p.ID + '_jk_all.counts.dat'
        cmd = ('./counts ' + data_filename + ' ' + bins_filename
               + ' > ' + counts_filename)
        os.system(cmd)
        counts_all = numpy.loadtxt(counts_filename, comments='#')

        # counting pairs for each jackknife sample
        for i in range(config.N_jackknife):
            jackknife_filename = config.jk_dir + 'uniform_' + p.ID + '_jk_' + str(i) + '.dat'
            counts_filename = config.jk_dir + 'uniform_' + p.ID + '_jk_' + str(i) + '.counts.dat'
            cmd = ('./counts ' + jackknife_filename + ' ' + bins_filename
                   + ' > ' + counts_filename)
            os.system(cmd)

        # calculate jackknife errors
        counts_list = []
        for i in range(config.N_jackknife):
            counts_filename = config.jk_dir + 'uniform_' + p.ID + '_jk_' + str(i) + '.counts.dat'
            counts_list.append(numpy.loadtxt(counts_filename, comments='#'))

        N_rbins = len(bins_list)
        N_jk = config.N_jackknife

        jk_mean = [0.0 for k in range(N_rbins)]
        jk_std = [0.0 for k in range(N_rbins)]

        for k in range(N_rbins):
            for i in range(N_jk):
                jk_mean[k] += counts_list[i][k][4]
            jk_mean[k] /= N_jk

            for i in range(N_jk):
                jk_std[k] += (counts_list[i][k][4] - jk_mean[k])**2
            jk_std[k] = math.sqrt(jk_std[k] * (N_jk - 1) / N_jk)

        output_filename = config.jk_dir + 'uniform_' + p.ID + '_jk_error.dat'
        output_file = open(output_filename, 'w')
        for k in range(N_rbins):
            r_lower = counts_all[k][0]
            r_upper = counts_all[k][1]
            r_middle = counts_all[k][2]
            dr = counts_all[k][3]
            counts = counts_all[k][4]
            corr = counts_all[k][5]
            # check if the total counts is zero.
            # if so, set jackknife error to zero,
            # and this point should be excluded when doing mcmc.
            if counts == 0:
                err_jk = 0.0
            else:
                # This is actually a fractional error of pair counting
                # When dealing with correlation function measurement, the final error
                # should be this fractional error times the weighted measurement.
                err_jk = jk_std[k] / counts

            output_file.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{:e}\n'
                              .format(r_lower, r_upper, r_middle, dr,
                                      jk_mean[k], jk_std[k], counts, err_jk))

        output_file.close()


if __name__ == '__main__':
    main()

