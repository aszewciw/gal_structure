from config import *

def main():

    # Load data generated from c files
    thin_file = data_dir + 'mock_thin.dat'
    thick_file = data_dir + 'mock_thick.dat'

    test = 'thick'
    # test = 'thin'

    if test == 'thick':
        Z, R, x, y, z = np.genfromtxt(thick_file, unpack=True,
            usecols=[0, 1, 8, 9, 10])
    if test == 'thin':
        Z, R, x, y, z = np.genfromtxt(thin_file, unpack=True,
            usecols=[0, 1, 8, 9, 10])

    N_points = len(x)
    # N_points = 10

    tolerance = 1e-5

    z_count = 0
    r_count = 0

    Z_new = np.zeros(N_points)
    R_new = np.zeros(N_points)
    for i in range(N_points):
        ra, dec, r = cart2eq(x[i], y[i], z[i])
        l, b = eq2gal(ra, dec)
        Z_new[i], R_new[i] = gal2ZR(l, b, r)
        z_diff = abs(Z_new[i] - Z[i])
        r_diff = abs(R_new[i] - R[i])

        if z_diff > tolerance:
            z_count +=1
        if r_diff > tolerance:
            r_count +=1

    print(z_count, r_count)

    index = np.argmax(abs(Z_new - Z))

    print(Z[index], Z_new[index])
    # print(max(Z_new - Z), min(Z_new - Z))
    # print(max(R_new - R), min(R_new - R))


if __name__ == '__main__':
    main()