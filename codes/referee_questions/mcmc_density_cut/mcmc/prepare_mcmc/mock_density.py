'''
For each l.o.s., calculate the density in different subvolumes of the pointing.
Then normalize each density by the average density in the whole pointing.
'''
from config import *

def main():

    # load the todo pointing list
    input_filename = rawdata_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    # load the bins list
    bins_file = rbins_dir + 'rbins.dat'
    rlower, rupper, volume = np.genfromtxt(bins_file, skip_header=1,
        unpack=True)

    # get volume of whole pointing
    volume_los = np.sum(volume)

    Nbins = len(rlower)

    for p in todo_list:

        # a progress indicator
        if todo_list.index(p) % 10 == 0:
            sys.stderr.write('On pointing #{} of {} ..\n'
                             .format(todo_list.index(p), len(todo_list)))

        mock_file = mock_dir + 'mock_' + p.ID + '.xyz.dat'
        x,y,z     = np.genfromtxt(mock_file, skip_header=1, unpack=True)
        distance  = np.sqrt(x**2 + y**2 + z**2)

        counts = np.zeros(Nbins)

        for i in range(Nbins):

            r1 = rlower[i]
            r2 = rupper[i]

            counts[i] = len( np.where((distance>r1)&(distance<=r2))[0] )

        # raw density in each subvolume
        density_real = counts / volume

        # average density in whole l.o.s.
        N_points = len(distance)
        density_los = N_points / volume_los

        # Normalize density and add to array
        density_norm = density_real / density_los

        output_file = density_dir + 'density_norm_' + p.ID + '.dat'

        np.savetxt(output_file, density_norm)


if __name__ == '__main__':
    main()