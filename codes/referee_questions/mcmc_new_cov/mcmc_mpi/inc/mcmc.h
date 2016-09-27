#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>
#include <math.h>
#include <time.h>
#include <string.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_integration.h>
#include <mpi.h>

/* I/O directories */
#define RAW_DIR "../../data/"
#define DATA_DIR "../data/"
#define DD_DIR "../data/mock_dd/"
#define ERR_DIR "../data/errors/"
#define OUT_DIR "../data/mcmc_output/"
#define PAIRS_DIR "../data/model_pairs/"
#define ZRW_DIR "../data/model_positions/"
#define BINS_DIR "../data/rbins/"
#define UNI_DIR "../data/uniform_dir/"

/* Arguments optionally passed via command line */
typedef struct {
  int N_params;       /* number of parameters */
  long double r0_thin;     /* thin disk scale length */
  long double z0_thin;     /* thin disk scale height */
  long double r0_thick;    /* thick disk scale length */
  long double z0_thick;    /* thick disk scale height */
  long double ratio;       /* thick:thin number density ratio */
  char filename[256]; /* name of output file */
  int max_steps;      /* max steps in MCMC chain */
} ARGS;

/* Data for each radial bin */
typedef struct {
  char binID[256];      /* ID for each radial bin */
  long double DD;            /* segue pair counts */
  long double MM;            /* model pair counts */
  // long double RR;            /* uniform pair counts */
  long double frac_error;    /* fractional error in model */
  // long double sigma;         /* sigma for MM, weighted by MM */
  unsigned int N_pairs; /* number of unique pairs */
  int * pair1;          /* array of pair1 index of length N_pairs */
  int * pair2;          /* array of pair2 index of length N_pairs */
} RBIN;

/* Inverted correlation matrix -- accessed as cor_row[i].cor_col[j] */
typedef struct {
  long double * invcor_col; /* each column value corresponding to a row value */
} INVCOR;

/* Pointing line of sight in sky */
typedef struct {
  char ID[256];         /* Unique ID for pointing */
  int N_stars;          /* Number of stars in model sample */
  long double * Z;           /* array of star heights above gal plane */
  long double * R;           /* array of star distances from gal center in gal plane */
  long double * weight;      /* star's density weight based on Z, R */
  RBIN * rbin;          /* Nbins of these structures */
  INVCOR * invcor_row;  /* Inverted correlation matrix: first index is a row */
} POINTING;

/* Data for each step in MCMC chain */
typedef struct {
  long double r0_thin;           /* thin disk scale length */
  long double z0_thin;           /* thin disk scale height */
  long double r0_thick;          /* thick disk scale length */
  long double z0_thick;          /* thick disk scale height */
  long double ratio_thick_thin;  /* number density ratio */
  long double chi2;              /* total chi2 for step */
  long double chi2_reduced;      /* chi2/DOF */
} STEP_DATA;

/* I/O functions */
ARGS parse_command_line( int n_args, char ** arg_array );
void load_pointingID(int *N_plist, POINTING **plist);
int load_Nbins(void);
void load_ZRW(POINTING *plist, int lower_ind, int upper_ind, int rank);
void load_rbins(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank);
void load_pairs(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank);
void load_inv_correlation(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank);
void output_mcmc(int index, STEP_DATA p, FILE *output_file);

/* Stats functions */
long double calculate_chi2(POINTING *p, int N_bins, int lower_ind, int upper_ind);

/* MCMC functions */
void set_weights(STEP_DATA params, POINTING *p, int lower_ind, int upper_ind);
long double normalize_MM(long double *weight, int N_stars);
long double calculate_MM( unsigned int N_pairs, int *pair1, int *pair2, long double MM_norm,
  long double *weight );
void update_model(POINTING *p, int N_bins, int lower_ind, int upper_ind);
// void calculate_correlation(POINTING *p, int N_bins, int lower_ind, int upper_ind);
int degrees_of_freedom(POINTING *p, int N_bins, int lower_ind, int upper_ind);
STEP_DATA update_parameters(STEP_DATA p, gsl_rng * GSL_r);
void run_mcmc(POINTING *plist, int N_params, STEP_DATA initial, int N_bins, int max_steps,
    int lower_ind, int upper_ind, int rank, int nprocs, char filename[256]);

/* Other */
long double sech2(long double x);