#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>
#include <math.h>
#include <time.h>
#include <string.h>

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

    // /* Angles in radians */
    // /* Galactic longitude (in plane angle) */
    // double gal_l_rad;
    // /* Galactic latitude (above/below plane angle) */
    // double gal_b_rad;
    // /* Right Ascension */
    // double ra_rad;
    // /* Declination */
    // double dec_rad;
    // /* distance from sun to star */
    // double distance;
    // /* cartesian x from ra, dec */
    // double x;
    // /* cartesian y from ra, dec */
    // double y;
    // /* cartesian z from ra, dec */
    // double z;

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
    /* current number of data points in mock l.o.s. */
    int N_mock;
    /* Set=0 until N_mock >= N_data. Then set=1 */
    int flag;

} POINTING;

/* ---------------------------------------------------------------- */

/* A structure used to test the density */
typedef struct DVOL{

    /* radial minimum in plane */
    double r_min;
    /* radial maximum */
    double r_max;
    /* height minimum */
    double z_min;
    /* height maximum */
    double z_max;
    /* angle min */
    double phi_min;
    /* angle max */
    double phi_max;
    /* angle range */
    double phi_range;
    /* volume of element */
    double volume;
    /* raw counts of stars in element */
    int N_raw;

} DVOL;

/* ---------------------------------------------------------------- */
/* -------------------------- FUNCTIONS --------------------------- */
/* ---------------------------------------------------------------- */


/* I/O functions */
void load_pointing_list(int *N_plist, POINTING **plist);
void get_params( PARAMS *p, unsigned long int N );
double integrate_Z(double z0, double z_min, double z_max);
double integrate_R(double r0, double r_min, double r_max);
void output_data( FILE *output_file, double density_analytic,
    double density_mock, DVOL vol);

/* Generation of stars */
double random_gal_Z(double z0, double pdf_norm, double z_min, double z_max);
double random_gal_R(double r0, double pdf_norm, double r_min, double r_max);
void generate_stars( STAR *s, PARAMS *p, int disk_type );

/* Used in calculation of density */
void get_volume(DVOL *dv, PARAMS *p);
double integrate_Z_term(double z0, double z_min, double z_max);
double integrate_R_term(double r0, double r_min, double r_max);
double ave_dens_analytic(PARAMS *p, DVOL *dv, unsigned long int N_stars);
double ave_dens_sample(PARAMS *p, DVOL *dv, STAR *thin, STAR *thick);
