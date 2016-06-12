import os, sys, random
import string, csv
import pickle
import numpy as np


PLATE_RADIUS_DEGREES = 1.49 # the radius of the plate, in degrees
PLATE_RADIUS_RADIANS = np.radians(PLATE_RADIUS_DEGREES)

#control the inner and outer limit of the sample to be used.
INNER_DISTANCE_LIMIT = 1.0
OUTER_DISTANCE_LIMIT = 3.0

rawdata_dir = '../../data/'
data_dir    = './data/'

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
def cart2eq(x, y, z):
    """
    Convert Cartesian coordinates to Equatorial coordinates

    Keywords arguments:
    x -- x coordinate
    y -- y coordinate
    z -- z coordinate

    Return a tuple (ra, dec, z):
    ra  -- Right Ascension (in radians)
    dec -- Declination (in radians)
    """

    r   = np.sqrt(x * x + y * y + z * z)
    ra  = np.arctan2(y, x)

    for i in range(len(ra)):
        if ra[i]>=0.0:
            continue
        else:
            ra[i]+=2.0*np.pi

    dec = np.arcsin(z / r)

    return ra, dec
#------------------------------------------------------------------------------
# RA(radians),Dec(radians),distance(kpc) of Galactic center in J2000
Galactic_Center_Equatorial=(np.radians(266.40510), np.radians(-28.936175), 8.33)

# RA(radians),Dec(radians) of Galactic Northpole in J2000
Galactic_Northpole_Equatorial=(np.radians(192.859508), np.radians(27.128336))
Galactic_Ascending_Node = np.radians(32.932)
#------------------------------------------------------------------------------
def eq2gal(ra,dec):
    """
    Convert Equatorial coordinates to Galactic Coordinates in the epch J2000.

    Keywords arguments:
    ra  -- Right Ascension (in radians)
    dec -- Declination (in radians)

    Return a tuple (l, b):
    l -- Galactic longitude (in radians)
    b -- Galactic latitude (in radians)
    """

    alpha = Galactic_Northpole_Equatorial[0]
    delta = Galactic_Northpole_Equatorial[1]
    la    = Galactic_Ascending_Node

    b = np.arcsin( np.sin(dec) * np.sin(delta)
        + np.cos(dec) * np.cos(delta) * np.cos(ra - alpha) )

    l = np.arctan2( np.sin(dec) * np.cos(delta)
        - np.cos(dec) * np.sin(delta) * np.cos(ra - alpha),
        np.cos(dec) * np.sin(ra - alpha) ) + la

    for i in range(len(l)):

        if l[i]>=0:
            continue
        else:
            l[i] += np.pi*2.0

    l = l % (2.0 * np.pi)

    return l, b
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
    la    = Galactic_Ascending_Node

    dec = ( np.arcsin( np.sin(b) * np.sin(delta)
        + np.cos(b) * np.cos(delta) * np.sin(l-la) ) )

    ra = ( np.arctan2( np.cos(b) * np.cos(l - la),
        np.sin(b) * np.cos(delta) - np.cos(b) * np.sin(delta)
        * np.sin(l - la) ) + alpha )


    for i in range(len(ra)):
        if ra[i]>=0:
            continue
        else:
            ra[i] += np.pi * 2.0

    ra = ra % (2.0 * np.pi)

    return ra, dec
#------------------------------------------------------------------------------
# sun's distance away from the galactic center
Galactic_Sun_Position = 8.0

def gal2ZR(l, b, distance):
    """
    Transfer helio-centered galactic coordinates to galactic center based
    z and r (cylinder coordinates).
    Used to put into the galactic disk model to calculate the density.

    Keywords arguments:
    l -- Galactic longitude (in radians)
    b -- Galactic latitude (in radians)

    Return numpy arrays (Z, R):
    Z  -- absolute distance above/below the galactic disk
    R -- distance away from the galactic center axis
    """

    # z projection
    Z = abs(distance * np.sin(b))
    # Law of cosines
    x = distance * np.cos(b)
    y = Galactic_Sun_Position
    R = np.sqrt(x * x + y * y - 2.0 * x * y * np.cos(l))

    return Z, R
