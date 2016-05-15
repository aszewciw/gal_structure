#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>
#include <math.h>
#include <time.h>
#include <string.h>

/* Directories */
#define OUT_DIR "./data/"
#define REF_DIR "../data/"

/* Different coordinate data of a given star */
typedef struct STAR{
    long double gal_z, gal_r, gal_phi; // gal-centered gal coord.
    long double gal_l_rad, gal_b_rad; // sun-centered gal coord.
    long double ra_rad, dec_rad, distance; // sun-centered equatorial coord.
    long double x, y, z; // sun-centered (equatorial/cartesian)
} STAR;

/* Conversions between coordinates systems */
long double get_distance(long double Z, long double R, long double phi);
void ZR_to_gal(STAR *s);
void gal_to_eq(STAR *s);
void eq_to_cart(STAR *s);

/* Generation of random values */
long double random_gal_Z(long double z0, long double pdf_norm, long double z_min, long double z_max);
long double random_gal_R(long double r0, long double pdf_norm, long double r_min, long double r_max);