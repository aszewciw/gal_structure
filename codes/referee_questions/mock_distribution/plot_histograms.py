import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def main():

    data_dir = './prepare_mock/data/'
    comp_file = data_dir + 'all_stars.dat'
    samp_file = data_dir + 'selected_stars.dat'



    disk_samp, Z_samp, R_samp = np.genfromtxt(samp_file, unpack=True)

    thin_ind  = np.where(disk_samp==0)[0]
    thick_ind = np.where(disk_samp==1)[0]

    Zthinsamp  = Z_samp[thin_ind]
    Rthinsamp  = R_samp[thin_ind]
    Zthicksamp = Z_samp[thick_ind]
    Rthicksamp = R_samp[thick_ind]

    thin_frac = len(thin_ind) / len(disk_samp)
    thick_frac = len(thick_ind) / len(disk_samp)

    thin_label = 'Thin: ' + str(np.round(thin_frac, 3))
    thick_label = 'Thick: ' + str(np.round(thick_frac, 3))

    plt.clf()
    plt.figure(1)
    n, bins, patches = plt.hist(Zthinsamp, 50, facecolor='green', alpha=0.5, label=thin_label)
    n, bins, patches = plt.hist(Zthicksamp, 50, facecolor='red', alpha=0.5, label=thick_label)
    plt.xlabel('Z (kpc)')
    plt.ylabel(r'$N_{stars}$', fontsize=16)
    plt.legend(loc=0)
    plt.title('Sample Distribution')
    plt.savefig('zsamp.png')
    # plt.figure(2)
    # n, bins, patches = plt.hist(Rthinsamp, 50, facecolor='green', alpha=0.5)
    # n, bins, patches = plt.hist(Rthicksamp, 50, facecolor='red', alpha=0.5)
    # plt.savefig('rsamp.png')



    # disk_all, Z_all, R_all = np.genfromtxt(comp_file, unpack=True)

    # thin_ind  = np.where(disk_all==0)[0]
    # thick_ind = np.where(disk_all==1)[0]

    # Zthinall  = Z_all[thin_ind]
    # Rthinall  = R_all[thin_ind]
    # Zthickall = Z_all[thick_ind]
    # Rthickall = R_all[thick_ind]

    # plt.figure(3)
    # n, bins, patches = plt.hist(Zthinall, 50, facecolor='green', alpha=0.5)
    # n, bins, patches = plt.hist(Zthickall, 50, facecolor='red', alpha=0.5)
    # plt.savefig('zall.png')
    # plt.figure(4)
    # n, bins, patches = plt.hist(Rthinall, 50, facecolor='green', alpha=0.5)
    # n, bins, patches = plt.hist(Rthickall, 50, facecolor='red', alpha=0.5)
    # plt.savefig('rall.png')

if __name__ == '__main__':
    main()