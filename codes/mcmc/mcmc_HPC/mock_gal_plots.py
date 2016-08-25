import numpy as np
import matplotlib.pyplot as plt
import math

#------------------------------------------------------------------------------

def random_Z(Z_0, pdf_norm, Z_max, Z_min, N_stars):

    cdf = np.random.rand(N_stars)

    b = math.tanh(Z_min / 2 / Z_0)
    temp = cdf * (pdf_norm * 2 * Z_0)**-1 + b
    Z = np.arctanh(temp) * 2 * Z_0

    # Generate random positive or negative 1
    plus_minus = 2 * np.random.randint(2, size=N_stars) - 1
    Z *= plus_minus

    return Z

#------------------------------------------------------------------------------

def random_R(R_0, pdf_norm, R_max, R_min, N_stars):

    cdf = np.random.rand(N_stars)

    b = math.exp(-R_min / R_0)
    exp_term = b - cdf * (pdf_norm * R_0)**-1
    R = -R_0 * np.log(exp_term)

    return R

#------------------------------------------------------------------------------

# Scale Heights and Lengths
# thick_sc_he      = 0.674
# thick_sc_le      = 2.51
# thin_sc_he       = 0.233
# thin_sc_le       = 2.34
# thick_thin_ratio = 0.1

thick_sc_he      = 0.5
thick_sc_le      = 2
thin_sc_he       = 0.3
thin_sc_le       = 2
thick_thin_ratio = 0.4

# Number of each disk
N_stars = 1000000
N_stars_thick = int(thick_thin_ratio * N_stars)
N_stars_thin  = N_stars - N_stars_thick

# R, Z, and phi limits for random generation
R_min = 1
R_max = 12
Z_min = 0
Z_max = 3
phi_min = 0
phi_max = 2 * math.pi
phi_range = phi_max - phi_min

# Normalization of PDFs
r_thick_norm  = 1 / ( thick_sc_le * ( math.exp( -R_min / thick_sc_le )
    - math.exp( -R_max / thick_sc_le ) ) )
z_norm_thick  = 1 / ( 2 * thick_sc_he * ( math.tanh( Z_max / 2 / thick_sc_he )
    - math.tanh( -Z_min / thick_sc_he ) ) )
r_thin_norm   = 1 / ( thin_sc_le * ( math.exp( -R_min / thin_sc_le )
    - math.exp( -R_max / thin_sc_le ) ) )
z_norm_thin   = 1 / ( 2 * thin_sc_he * ( math.tanh( Z_max / 2 / thin_sc_he )
    - math.tanh( -Z_min / thin_sc_he ) ) )


###########################################################
##################-- Star Positions --#####################
###########################################################

"""
Galactic Coordinates - Centered on MW Center
+x axis points away from Sun
"""

# Thin Disk
Z_thin_gal = random_Z(thin_sc_he, z_norm_thin, Z_max, Z_min, N_stars_thin)
R_thin_gal = random_R(thin_sc_le, r_thin_norm, R_max, R_min, N_stars_thin)
phi_thin   = phi_min + phi_range * np.random.rand(N_stars_thin)
x_thin_gal = R_thin_gal * np.cos(phi_thin)
y_thin_gal = R_thin_gal * np.sin(phi_thin)

# Thick Disk
Z_thick_gal = random_Z(thick_sc_he, z_norm_thick, Z_max, Z_min, N_stars_thick)
R_thick_gal = random_R(thick_sc_le, r_thick_norm, R_max, R_min, N_stars_thick)
phi_thick   = phi_min + phi_range * np.random.rand(N_stars_thick)
x_thick_gal = R_thick_gal * np.cos(phi_thick)
y_thick_gal = R_thick_gal * np.sin(phi_thick)

plt.figure(1)
plt.subplot(211, aspect='equal')
plt.scatter(x_thin_gal, Z_thin_gal, c='blue', s=3)
plt.xlabel('Radius R (kpc)')
plt.ylabel('Height Z (kpc)')
plt.title('Mock Galaxy - Thin Disk')
plt.axis([-12, 12, -3, 3])


plt.subplot(212, aspect='equal')
plt.scatter(x_thick_gal, Z_thick_gal, c='red', s=3)
plt.xlabel('Radius R (kpc)')
plt.ylabel('Height Z (kpc)')
plt.title('Mock Galaxy - Thick Disk')
plt.axis([-12, 12, -3, 3])
# plt.savefig('mock1.png')
plt.savefig('mock2.png')

# plt.show()