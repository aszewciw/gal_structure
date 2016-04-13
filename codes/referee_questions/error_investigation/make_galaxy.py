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

#------------------------------------------------------------------------------

# RA(radians),Dec(radians),distance(kpc) of Galactic center in J2000
Galactic_Center_Equatorial=(math.radians(266.40510), math.radians(-28.936175), 8.33)

# RA(radians),Dec(radians) of Galactic Northpole in J2000
Galactic_Northpole_Equatorial=(math.radians(192.859508), math.radians(27.128336))
Galactic_Ascending_Node = math.radians(32.932)

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

def galCent_to_sunCent(x, y, z, R_solar):

    distance = ( (x-R_solar)**2 + y**2 + z**2 ) ** 0.5

    l = np.arctan2(y, x-R_solar)
    b = np.arcsin(z / distance)

    for i in l:
        if i>=0:
            continue
        else:
            i+= math.pi * 2

    l = l % (2.0 * math.pi)

    return distance, l, b


#------------------------------------------------------------------------------
def gal2eq(l, b):
    """
    Convert Galatic coordinates to Equatorial Coordinates in the epch J2000.

    Keywords arguments:
    l -- Galactic longitude (in radians)
    b -- Galactic latitude (in radians)

    Return a tuple (ra, dec):
    ra  -- Right Ascension (in radians)
    dec -- Declination (in radians)
    """

    alpha = Galactic_Northpole_Equatorial[0]
    delta = Galactic_Northpole_Equatorial[1]
    la = Galactic_Ascending_Node

    dec = np.arcsin(np.sin(b) * np.sin(delta) +
                    np.cos(b) * np.cos(delta) * np.sin(l - la))

    ra = np.arctan2(np.cos(b) * np.cos(l - la),
                    np.sin(b) * np.cos(delta) -
                    np.cos(b) * np.sin(delta) * np.sin(l - la)
                    ) + alpha

    for i in ra:
        if i>=0:
            continue
        else:
            i+= math.pi * 2

    ra = ra % (2.0 * math.pi)

    return ra, dec
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def eq2cart(ra, dec, r):
    """
    Convert Equatorial coordinates to Cartesian coordinates.
    Return a tuple (x, y, z) in the same unit of the input distance.

    Keywords arguments:
    ra  -- Right Ascension (in radians)
    dec -- Declination (in radians)
    r   -- Distance

    """

    x = r * np.cos(ra) * np.cos(dec)
    y = r * np.sin(ra) * np.cos(dec)
    z = r * np.sin(dec)

    return x, y, z
#------------------------------------------------------------------------------
# def main():

###########################################################
#################-- Disk Parameters --#####################
###########################################################

# Scale Heights and Lengths
thick_sc_he      = 0.674
thick_sc_le      = 2.51
thin_sc_he       = 0.233
thin_sc_le       = 2.34
thick_thin_ratio = 0.06

# Number of each disk
N_stars       = 1000000
N_stars_thick = int(thick_thin_ratio * N_stars)
N_stars_thin  = N_stars - N_stars_thick

# R, Z, and phi limits for random generation
R_min = 5
R_max = 11
Z_min = 0
Z_max = 3
phi_max   = math.atan(0.5)
phi_min   = -phi_max
phi_min   += math.pi
phi_max   += math.pi
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

'''
Now move everything to sun-centered systems'''

# Some question as to whether or not to include a Z for the sun.
# I'll proceed without doing so for now
R_sun = -8.0

# Thin Disk
r_thin_sun, l_thin, b_thin = galCent_to_sunCent(x_thin_gal, y_thin_gal, Z_thin_gal, R_sun)
ra_thin, dec_thin          = gal2eq(l_thin, b_thin)
x_thin, y_thin, z_thin     = eq2cart(ra_thin, dec_thin, r_thin_sun)

# Thick Disk
r_thick_sun, l_thick, b_thick = galCent_to_sunCent(x_thick_gal, y_thick_gal, Z_thick_gal, R_sun)
ra_thick, dec_thick           = gal2eq(l_thick, b_thick)
x_thick, y_thick, z_thick     = eq2cart(ra_thick, dec_thick, r_thick_sun)


# np.savez_compressed('thick_disk_smallmock.npz',
#     x_thick=x_thick, y_thick=y_thick, z_thick=z_thick,
#     ra_thick=ra_thick, dec_thick=dec_thick, r_thick_sun=r_thick_sun,
#     Z_thick_gal=Z_thick_gal, R_thick_gal=R_thick_gal, l_thick=l_thick,
#     b_thick=b_thick, x_thick_gal=x_thick_gal, y_thick_gal=y_thick_gal)

# np.savez_compressed('thin_disk_smallmock.npz',
#     x_thin=x_thin, y_thin=y_thin, z_thin=z_thin,
#     ra_thin=ra_thin, dec_thin=dec_thin, r_thin_sun=r_thin_sun,
#     Z_thin_gal=Z_thin_gal, R_thin_gal=R_thin_gal, l_thin=l_thin,
#     b_thin=b_thin, x_thin_gal=x_thin_gal, y_thin_gal=y_thin_gal)

print('Files Written')