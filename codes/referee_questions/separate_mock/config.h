#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>
#include <math.h>
#include <time.h>
#include <string.h>

/* Directories */
// #define OUT_DIR "./data/"
// #define REF_DIR "../data/"
#define DATA_DIR "../prepare_mock/data/"
#define OUT_DIR "../data/"

#define PLATE_RADIUS_DEG 1.49

/* vector for use in dot product */
typedef struct VECTOR{
    long double x, y, z;
} VECTOR;

/* Different coordinate data of a given star */
typedef struct STAR{
    long double gal_z, gal_r, gal_phi; // gal-centered gal coord.
    long double gal_l_rad, gal_b_rad; // sun-centered gal coord.
    long double ra_rad, dec_rad, distance; // sun-centered equatorial coord.
    long double x, y, z; // sun-centered (equatorial/cartesian)
} STAR;

/* A structure for a plate pointing to the sky */
typedef struct POINTING{
    char ID[256];
    long double ra_deg, dec_deg, ra_rad, dec_rad;
    long double galactic_l_rad, galactic_b_rad;
    long double x, y, z;   /* Cartesians on unit sphere */
    long double r_min, r_max;      /* distances range */
    int N_data, N_mock; /* number of stars */
} POINTING;

/* I/O functions */
void load_pointing_list(int *N_plist, POINTING **plist);
void load_mock_thin(unsigned long int *N_stars, STAR **thin);
void load_mock_thick(unsigned long int *N_stars, STAR **thick);

long double dot_product(VECTOR v1, VECTOR v2);
void separate_sample(POINTING *p, STAR *s, int N_p, unsigned long int N_s);
