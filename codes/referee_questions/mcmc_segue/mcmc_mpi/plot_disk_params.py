#!/usr/bin/env python
'''
Create plots for an MCMC chain.

For a list of MCMC data files, create the following plots:
1. r0_thick vs r0_thin (contour)
2. z0_thick vs z0_thin (contour)
3. chi2 color-barred steps for each parameter

My MCMC files output the following columns:
    step number
    chi2
    reduced chi2
    r0_thin
    z0_thin
    r0_thick
    z0_thick
    thick_thin_ratio
'''

# from custom_plotting import mcmc_plot as mcpl
import matplotlib.pyplot as plt
import corner
import pandas as pd
import sys
import numpy as np

# "True" parameters for use mainly in mock contour plots
z0_thin_true  = 0.233
r0_thin_true  = 2.34
z0_thick_true = 0.674
r0_thick_true = 2.51
ratio_true    = 0.1

def plot_mcmc_steps(DF, outfile, ticks):
    '''
    Plot the chi2 coloring
    '''
    plt.clf()

    plt.subplot(321)
    # plt.ylabel("$Z_{0,thin} (kpc)$")
    plt.ylabel('z0 thin')
    plt.scatter(DF['step'].values, DF['z0_thin'].values, c=DF['chi2'].values, s=2)
    plt.axis([0, DF['step'].values[-1], min(DF['z0_thin']), max(DF['z0_thin'])])
    plt.xticks(ticks)

    plt.subplot(322)
    # plt.ylabel("$Z_{0,thick} (kpc)$")
    plt.ylabel('z0 thick')
    plt.scatter(DF['step'].values, DF['z0_thick'].values, c=DF['chi2'].values, s=2)
    plt.axis([0, DF['step'].values[-1], min(DF['z0_thick']), max(DF['z0_thick'])])
    plt.xticks(ticks)

    plt.subplot(323)
    # plt.ylabel("$R_{0,thin} (kpc)$")
    plt.ylabel('r0 thin')
    plt.scatter(DF['step'].values, DF['r0_thin'].values, c=DF['chi2'].values, s=2)
    plt.axis([0, DF['step'].values[-1], min(DF['r0_thin']), max(DF['r0_thin'])])

    plt.subplot(324)
    plt.xlabel("Loop Number")
    # plt.ylabel("$R_{0,thick} (kpc)$")
    plt.ylabel('r0 thick')
    plt.scatter(DF['step'].values, DF['r0_thick'].values, c=DF['chi2'].values, s=2)
    plt.axis([0, DF['step'].values[-1], min(DF['r0_thick']), max(DF['r0_thick'])])
    plt.xticks(ticks)

    plt.subplot(325)
    plt.xlabel("Loop Number")
    # plt.ylabel(r"$\displaystyle\frac{n_{thick}}{n_{thin}}$")
    plt.ylabel('thick to thin ratio')
    plt.scatter(DF['step'].values, DF['z0_thin'].values, c=DF['chi2'].values, s=2)
    plt.axis([0, DF['step'].values[-1], min(DF['z0_thin']), max(DF['z0_thin'])])
    plt.xticks(ticks)
    plt.colorbar()

    plt.savefig(outfile)


def main():

    # Create list of files for which we want plots
    filenames = ['mcmc_result.dat', 'mcmc_result_new.dat']

    # path to files
    data_path = '../data/mcmc_output/'
    plot_path = '../plots/'


    # Create plots for each file in list
    for f in filenames:

        # Remove .dat for naming of plots
        file_prefix = f.split('.')[0]

        # Choose file for reading
        file = data_path + f

        # Load MCMC data frame
        MCMC = pd.read_csv(file, sep='\s+')

        # Check that names were included in header
        # First column should be headers listed above
        if MCMC.columns[0]!='step':
            print('This file needs header names as its first row!')
            continue

        # Cut a fraction of the data as "burn-in"
        # Could improve method for deciding on this fraction
        frac_cut = 0.05
        N_drop   = len(MCMC) * frac_cut
        MCMC     = MCMC[MCMC['step']>N_drop]

        # Set significance levels for contour plots
        signif_levels = np.array([1.0,2.0,3.0])
        levels = 1.0 - np.exp(-0.5*signif_levels**2)

        print('Beginning Plotting...')
        # Plot scale heights
        plt.clf()
        x = np.column_stack((MCMC['z0_thin'].values, MCMC['z0_thick'].values))
        fig = corner.corner(x, levels=levels, labels=["$Z_{0,thin}$", "$Z_{0,thick}$"],
            truths=[z0_thin_true, z0_thick_true])
        fig.suptitle("SEGUE MCMC Results")
        plot_name = plot_path + file_prefix + '_z0.png'
        plt.savefig(plot_name)

        print('Finished plotting Scale Heights')

        # Plot scale lengths
        plt.clf()
        x = np.column_stack((MCMC['r0_thin'].values, MCMC['r0_thick'].values))
        fig = corner.corner(x, levels=levels, labels=["$R_{0,thin}$", "$R_{0,thick}$"],
            truths=[r0_thin_true, r0_thick_true])
        fig.suptitle("SEGUE MCMC Results")
        plot_name = plot_path + file_prefix + '_r0.png'
        plt.savefig(plot_name)

        print('Finished plotting Scale Lengths')

        # Plot steps
        # Create ticks
        tick_start = 0
        tick_end   = MCMC['step'].values[-1]
        tick_size  = 100000
        step_ticks = np.arange(tick_start, tick_end, tick_size)
        plot_name  = plot_path + file_prefix + '_steps.png'
        # plot_mcmc_steps(MCMC, plot_name, step_ticks)

        print('Finished plotting Steps...or did I? Welp, I am done plotting.')


if __name__ == '__main__':
    main()