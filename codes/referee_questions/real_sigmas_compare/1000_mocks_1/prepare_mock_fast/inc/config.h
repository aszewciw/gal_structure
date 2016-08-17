#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>
#include <math.h>
#include <time.h>
#include <string.h>
#include <mpi.h>

/* Directories */
#define DATA_DIR "../data/"
#define OUT_DIR "./data/"

/* radius of a SEGUE plate */
#define PLATE_RADIUS_DEG 1.49

/* ---------------------------------------------------------------- */
/* -------------------------- STRUCTURES -------------------------- */
/* ---------------------------------------------------------------- */

/* vector for use in dot product */
typedef struct VECTOR{

    /* Cartesian coordinate 1 */
    double x;
    /* Cartesian coordinate 2 */
    double y;
    /* Cartesian coordinate 3 */
    double z;

} VECTOR;

/* ---------------------------------------------------------------- */

/* parameters for a Milky Way 2-disk model */
typedef struct PARAMS{

    /* ----------------------------- */
    /* --- Thin disk parameters ---- */
    /* ----------------------------- */

    /* thin disk scale height */
    double z0_thin;
    /* thin disk scale length */
    double r0_thin;
    /* PDF normalization for thin height */
    double z0_pdf_norm_thin;
    /* PDF normalization for thin length */
    double r0_pdf_norm_thin;
    /* number of stars in thin disk */
    unsigned long int N_thin;

    /* ----------------------------- */
    /* --- Thick disk parameters --- */
    /* ----------------------------- */

    /* thick disk scale height */
    double z0_thick;
    /* thick disk scale length */
    double r0_thick;
    /* PDF normalization for thick height */
    double z0_pdf_norm_thick;
    /* PDF normalization for thick length */
    double r0_pdf_norm_thick;
    /* number of stars in thick disk */
    unsigned long int N_thick;

    /* ----------------------------- */
    /* ----- Shared parameters ----- */
    /* ----------------------------- */

    /* thick/thin number density ratio */
    double ratio;

    /* Geometric sample params */
    /* minimum height of sample */
    double z_min;
    /* maximum height of sample */
    double z_max;
    /* minimum length of sample */
    double r_min;
    /* maximum length of sample */
    double r_max;
    /* minimum angle in galactic disk */
    double phi_min;
    /* maximum angle in galactic disk */
    double phi_max;
    /* phi_max - phi_min */
    double phi_range;

} PARAMS;

/* ---------------------------------------------------------------- */

/* Different coordinate data of a given star */
typedef struct STAR{

    /* ----------------------------- */
    /* ------ Galaxy-centered ------ */
    /* ----------------------------- */

    /* Height above galactic plane */
    double gal_z;
    /* Distance from galactic center projected on galactic plane */
    double gal_r;
    /* Angle in galactic plane: phi=0 is away from sun */
    double gal_phi;

    /* ----------------------------- */
    /* -------- Sun-centered ------- */
    /* ----------------------------- */

    /* Angles in radians */
    /* Galactic longitude (in plane angle) */
    double gal_l_rad;
    /* Galactic latitude (above/below plane angle) */
    double gal_b_rad;
    /* Right Ascension */
    double ra_rad;
    /* Declination */
    double dec_rad;
    /* distance from sun to star */
    double distance;
    /* cartesian x from ra, dec */
    double x;
    /* cartesian y from ra, dec */
    double y;
    /* cartesian z from ra, dec */
    double z;

} STAR;

/* ---------------------------------------------------------------- */

/* A structure for a plate pointing to the sky */
typedef struct POINTING{

    /* plate identification number */
    char ID[256];
    /* Right ascension (degrees) */
    double ra_deg;
    /* Declination (degrees) */
    double dec_deg;
    /* Right ascension (radians) */
    double ra_rad;
    /* Declination (radians) */
    double dec_rad;
    /* Galactic longitude */
    double galactic_l_rad;
    /* Galactic latitude */
    double galactic_b_rad;
    /* unit cartesian x from ra, dec */
    double x;
    /* unit cartesian y from ra, dec */
    double y;
    /* unit cartesian z from ra, dec */
    double z;
    /* inner distance limit of sample */
    double r_min;
    /* outer distance limit of sample */
    double r_max;
    /* number of data points (post cleaning) in SEGUE l.o.s. */
    int N_data;
    /* real current number of data points in mock l.o.s. */
    int N_mock;
    /* number of data points in mock l.o.s. for temp gxy per process */
    int N_mock_proc;
    /* Set=0 until N_mock >= N_data. Then set=1 */
    int flag;

} POINTING;

/* ---------------------------------------------------------------- */
/* -------------------------- FUNCTIONS --------------------------- */
/* ---------------------------------------------------------------- */

/* Conversions between coordinates systems */
double get_distance(double Z, double R, double phi);
void ZR_to_gal(STAR *s);
void gal_to_eq(STAR *s);
void eq_to_cart(STAR *s);

/* I/O functions */
void load_pointing_list(int *N_plist, POINTING **plist, int rank);
double integrate_Z(double z0, double z_min, double z_max);
double integrate_R(double r0, double r_min, double r_max);
void get_params( PARAMS *p, unsigned long int N, int rank );
void output_star( FILE *output_file, STAR s );

/* Generation of stars */
double random_gal_Z(double z0, double pdf_norm, double z_min, double z_max);
double random_gal_R(double r0, double pdf_norm, double r_min, double r_max);
double dot_product(VECTOR v1, VECTOR v2);
void separate_sample(POINTING *p, STAR *s, int N_p, unsigned long int N_s, int rank,
    int mock_num);
void generate_stars( STAR *s, PARAMS *p, int disk_type );