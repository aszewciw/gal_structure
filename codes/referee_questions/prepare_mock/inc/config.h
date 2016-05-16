#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>
#include <math.h>
#include <time.h>
#include <string.h>

/* Directories */
// #define OUT_DIR "./data/"
// #define REF_DIR "../data/"
#define DATA_DIR "../data/"

#define PLATE_RADIUS_DEG 1.49

/* vector for use in dot product */
typedef struct VECTOR{
    double x, y, z;
} VECTOR;

/* parameters for a MW disk */
typedef struct PARAMS{
    double z0, r0; /* scale height, length */
    double z0_pdf_norm, r0_pdf_norm; /* pdf normalizations */
    double z_min, z_max, r_min, r_max, phi_min, phi_max, phi_range /* limits */
    double ratio; /* N_thick / N_thin */
    unsigned long int N_stars; /* Number of stars in disk */
} PARAMS;

/* Different coordinate data of a given star */
typedef struct STAR{
    double gal_z, gal_r, gal_phi; /* gal-centered gal coord. */
    double gal_l_rad, gal_b_rad; /* sun-centered gal coord. */
    double ra_rad, dec_rad, distance; /* un-centered equatorial coord. */
    double x, y, z; /* sun-centered (equatorial/cartesian) */
} STAR;

/* A structure for a plate pointing to the sky */
typedef struct POINTING{
    char ID[256];
    double ra_deg, dec_deg, ra_rad, dec_rad;
    double galactic_l_rad, galactic_b_rad;
    double x, y, z;   /* Cartesians on unit sphere */
    double r_min, r_max;      /* distances range */
    int N_data, N_mock; /* number of stars */
    int flag; /* Set=0 until N_mock >= N_data. Then set=1 */
} POINTING;

/* Conversions between coordinates systems */
double get_distance(double Z, double R, double phi);
void ZR_to_gal(STAR *s);
void gal_to_eq(STAR *s);
void eq_to_cart(STAR *s);

/* I/O functions */
void load_pointing_list(int *N_plist, POINTING **plist);
void get_thin_params( PARAMS *p, unsigned long int N );
void get_thick_params( PARAMS *p, unsigned long int N );

/* Generation of stars */
double random_gal_Z(double z0, double pdf_norm, double z_min, double z_max);
double random_gal_R(double r0, double pdf_norm, double r_min, double r_max);
double dot_product(VECTOR v1, VECTOR v2);
void separate_sample(POINTING *p, STAR *s, int N_p, unsigned long int N_s);
double dot_product(VECTOR v1, VECTOR v2);