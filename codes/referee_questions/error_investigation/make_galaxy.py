'''
Generates an entire Milky Way based on a two-disk model.
Model may be over dense (100 billion stars).
We will only extend 3 kpc beyond position of the sun so
that we fill a volume which contains our segue lines of
sight under rotation

NOTE: Don't run this on local machine. Only on bender.

'''
import numpy as np
import math
import matplotlib.pyplot as plt

# def random_Z(Z_0, Z_norm, Z_max, Z_min, N_stars):
def random_Z(Z_0, Z_norm, N_stars):

    CDF = np.random.rand(N_stars)
    # print(CDF * (Z_norm * 2 * Z_0)**-1 + np.tanh(Z_min * (2 * Z_0)**-1))
    # Z   = 2 * Z_0 * np.arctanh( CDF * (Z_norm * 2 * Z_0)**-1 + np.tanh(Z_min * (2 * Z_0)**-1) )
    Z   = 2 * Z_0 * np.arctanh(CDF)

    # Generate random positive or negative 1
    plus_minus = 2 * np.random.randint(2, size=N_stars) - 1
    Z *= plus_minus

    return Z

# def random_R(R_0, R_norm, R_max, R_min, N_stars):
def random_R(R_0, R_norm, N_stars):

    CDF = np.random.rand(N_stars)
    # R   = -R_0 * np.log( math.exp(-R_min / R_0) - CDF * (R_norm * R_0)**-1 )
    R   = -R_0 * np.log(1 - CDF)

    return R

def galCent_to_sunCent(x, y, z, R_solar):

    x -= R_solar
    distance = ( x**2 + y**2 + z**2 ) ** 0.5
    l = np.arctan(y / x)
    b = np.arcsin(z / distance)

    return distance, l, b
# def main():

    # Total stars to generate

np.random.seed()
N_stars          = 100000

# Galactic R,Z limits of sample
# NOTE: R, Z = 0 will be infinity
# R_min            = 0.1
# R_max            = 50
# Z_min            = 0.1
# Z_max            = 5

thick_sc_he      = 0.674
thick_sc_le      = 2.51
thin_sc_he       = 0.233
thin_sc_le       = 2.34
thick_thin_ratio = 0.06

N_stars_thick = int(thick_thin_ratio * N_stars)
N_stars_thin  = N_stars - N_stars_thick
# r_norm_thick  = 1 / ( thick_sc_le * ( math.exp( -R_min / thick_sc_le ) - math.exp( -R_max / thick_sc_le ) ) )
# z_norm_thick  = 1 / ( 2 * thick_sc_he * ( math.tanh( Z_max / 2 / thick_sc_he ) - math.tanh( -Z_min / thick_sc_he ) ) )
# r_norm_thin   = 1 / ( thin_sc_le * ( math.exp( -R_min / thin_sc_le ) - math.exp( -R_max / thin_sc_le ) ) )
# z_norm_thin   = 1 / ( 2 * thin_sc_he * ( math.tanh( Z_max / 2 / thin_sc_he ) - math.tanh( -Z_min / thin_sc_he ) ) )
r_norm_thin  = 1 / thin_sc_le
z_norm_thin  = 1 / thin_sc_he
r_norm_thick = 1 / thick_sc_le
z_norm_thick = 1 / thick_sc_he

# Z_thin  = random_Z(thin_sc_he, z_norm_thin, Z_max, Z_min, N_stars_thin)
# R_thin  = random_R(thin_sc_le, r_norm_thin, R_max, R_min, N_stars_thin)
# Z_thick = random_Z(thick_sc_he, z_norm_thick, Z_max, Z_min, N_stars_thick)
# R_thick = random_R(thick_sc_le, r_norm_thick, R_max, R_min, N_stars_thick)

Z_thin    = random_Z(thin_sc_he, z_norm_thin, N_stars_thin)
R_thin    = random_R(thin_sc_le, r_norm_thin, N_stars_thin)
Z_thick   = random_Z(thick_sc_he, z_norm_thick, N_stars_thick)
R_thick   = random_R(thick_sc_le, r_norm_thick, N_stars_thick)
phi_thin  = 2 * math.pi * np.random.rand(N_stars_thin)
phi_thick = 2 * math.pi * np.random.rand(N_stars_thick)

x_thin    = R_thin * np.cos(phi_thin)
y_thin    = R_thin * np.sin(phi_thin)

x_thick   = R_thick * np.cos(phi_thick)
y_thick   = R_thick * np.sin(phi_thick)

R_solar   = 8.0
dist_thin, l_thin, b_thin    = galCent_to_sunCent(x_thin, y_thin, Z_thin, R_solar)
dist_thick, l_thick, b_thick = galCent_to_sunCent(x_thick, y_thick, Z_thick, R_solar)

# plt.clf()
# # plt.scatter(x_thin, Z_thin, color='red', s=1)
# plt.scatter(x_thick, Z_thick, color='blue', s=3)
# plt.show()

# if __name__ == '__main__':
#     main()