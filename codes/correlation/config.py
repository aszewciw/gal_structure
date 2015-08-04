#!/usr/bin/env python

import os, sys, math, random
import string, csv
import pickle, cPickle

class Point:
    pass

class Star:
    pass

class Pointing:
    pass


PLATE_RADIUS_DEGREES = 1.49 # the radius of the plate, in degrees
PLATE_RADIUS_RADIANS = math.radians(PLATE_RADIUS_DEGREES)

#control the inner and outer limit of the sample to be used.
INNER_DISTANCE_LIMIT = 1.0
OUTER_DISTANCE_LIMIT = 3.0

rawdata_dir = '../data/'
data_dir = './data/'
plots_dir = './plots/'
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

    x = r * math.cos(ra) * math.cos(dec)
    y = r * math.sin(ra) * math.cos(dec)
    z = r * math.sin(dec)

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
    r   -- Distance in the same unit of input (x, y, z)
    """

    r = math.sqrt(x * x + y * y + z * z)
    ra = math.atan2(y, x)
    ra = ra if ra >= 0 else (2.0 * math.pi + ra)
    dec = math.asin(z / r)

    return ra, dec, r
#------------------------------------------------------------------------------
def dot(vec1, vec2):
    """
    Calculate the dot producs of 2 vectors in 3D Cartesian space.

    Keywords arguments:
    vec1 -- First vector in (x, y, z)
    vec2 -- Second vector in (x, y, z)

    Returns:
    dp -- the result of dot product
    """
    if len(vec1) is not 3 or len(vec2) is not 3:
        sys.stderr.write("Error: Wrong vector dimenson for dot product.\n")
        sys.exit()

    a1, a2, a3 = vec1[0], vec1[1], vec1[2]
    b1, b2, b3 = vec2[0], vec2[1], vec2[2]

    dp = a1 * b1 + a2 * b2 + a3 * b3

    return dp
#------------------------------------------------------------------------------
def cross(vec1, vec2):
    """
    Calculate the cross producs of 2 vectors in 3D Cartesian space.

    Keywords arguments:
    vec1 -- First vector in (x, y, z)
    vec2 -- Second vector in (x, y, z)

    Returns:
    vec -- the result vector in (x, y, z)
    """
    if len(vec1) is not 3 or len(vec2) is not 3:
        sys.stderr.write("Error: Wrong vector dimenson for cross product.\n")
        sys.exit()

    a1, a2, a3 = vec1[0], vec1[1], vec1[2]
    b1, b2, b3 = vec2[0], vec2[1], vec2[2]

    x = a2 * b3 - a3 * b2
    y = a3 * b1 - a1 * b3
    z = a1 * b2 - a2 * b1

    return x, y, z
#------------------------------------------------------------------------------
def rodrigues(axis, vec, theta):
    """
    Rotate a vector around an axis in 3D Cartesian space
    using Rodrigues' rotation formula.

    Keywords arguments:
    axis -- The vector of the axis in (x, y, z)
    vec  -- The vector to be rotated in (x, y, z)
    theta -- The rotation angle in radians.

    Return:
    vrot -- The rotated vector in (x, y, z)
    """
    # in case axis vector is a unit vector, normalize it.
    x0, y0, z0 = axis[0], axis[1], axis[2]

    r0 = math.sqrt(x0 * x0 + y0 * y0 + z0 * z0)

    x0 /= r0
    y0 /= r0
    z0 /= r0

    a = (x0, y0, z0)
    # cross product and dot product
    cp = cross(a, vec)
    dp = dot(a, vec)

    # rotation
    x = (vec[0] * math.cos(theta) + cp[0] * math.sin(theta)
         + x0 * dp * (1 - math.cos(theta)))

    y = (vec[1] * math.cos(theta) + cp[1] * math.sin(theta)
         + y0 * dp * (1 - math.cos(theta)))

    z = (vec[2] * math.cos(theta) + cp[2] * math.sin(theta)
         + z0 * dp * (1 - math.cos(theta)))

    return x, y, z
#------------------------------------------------------------------------------
