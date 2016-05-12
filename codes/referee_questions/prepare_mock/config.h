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
    double gal_z, gal_r, gal_phi, gal_x, gal_y; // gal-centered gal coord.
    double gal_l_rad, gal_b_rad; // sun-centered gal coord.
    double ra_rad, dec_rad, distance; // sun-centered equatorial coord.
    double x, y, z; // sun-centered (equatorial/cartesian)
} STAR;

/* Conversions between coordinates systems */
void ZR_to_gal(STAR *s);
void gal_to_eq(STAR *s);
void eq_to_cart(STAR *s);

/* Generation of random values */
double random_z(double z0, double pdf_norm, double z_min, double z_max);
double random_r(double r0, double pdf_norm, double r_min, double r_max);