import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def main():

    data_dir = './prepare_mock/data/'
    comp_file = data_dir + 'all_stars.dat'
    samp_file = data_dir + 'selected_stars.dat'

    # all_stars = np.genfromtxt(comp_file)
    disk_samp, Z_samp, R_samp = np.genfromtxt(samp_file, unpack=True)

    thin_ind  = np.where(disk_samp==0)[0]
    thick_ind = np.where(disk_samp==1)[0]

    Zthinsamp  = Z_samp[thin_ind]
    Rthinsamp  = R_samp[thin_ind]
    Zthicksamp = Z_samp[thick_ind]
    Rthicksamp = R_samp[thick_ind]

    plt.clf()
    plt.figure(1)
    n, bins, patches = plt.hist(Zthinsamp, 50, facecolor='green', alpha=0.5)
    n, bins, patches = plt.hist(Zthicksamp, 50, facecolor='red', alpha=0.5)
    plt.savefig('zsamp.png')
    plt.figure(2)
    n, bins, patches = plt.hist(Rthinsamp, 50, facecolor='green', alpha=0.5)
    n, bins, patches = plt.hist(Rthicksamp, 50, facecolor='red', alpha=0.5)
    plt.savefig('rsamp.png')

if __name__ == '__main__':
    main()