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
#define RR_DIR "../data/uniform_rr/"
#define ERR_DIR "../data/errors/"
#define OUT_DIR "../data/mcmc_output/"
#define PAIRS_DIR "../data/model_pairs/"
#define ZRW_DIR "../data/model_positions/"
#define BINS_DIR "../data/rbins/"


/* Data for each radial bin */
typedef struct {
  char binID[256];      /* ID for each radial bin */
  double DD;            /* mock pair counts */
  double MM;            /* model pair counts */
  double RR;            /* uniform pair counts */
  double DD_RR;         /* DD/RR */
  double MM_RR;         /* MM/RR */
  double diff;          /* DD/RR - MM/RR */
  unsigned int N_pairs; /* number of unique pairs */
  int * pair1;          /* array of pair1 index of length N_pairs */
  int * pair2;          /* array of pair2 index of length N_pairs */
} RBIN;

// /* A row of a matrix */
// typedef struct {
//   double * column;
// } ROW;

// /* A covariance matrix -- accessed as cov_row[i].cov_col[j] */
// typedef struct {
//   double * cov_col; /* each column value corresponding to a row value */
// } COV;

/* Inverted covariance matrix -- accessed as cov_row[i].cov_col[j] */
typedef struct {
  double * invcov_col; /* each column value corresponding to a row value */
} INVCOV;

// /* A correlation matrix -- accessed as cor_row[i].cor_col[j] */
// typedef struct {
//   double * cor_col; /* each column value corresponding to a row value */
// } COR;

/* Pointing line of sight in sky */
typedef struct {
  char ID[256];     /* Unique ID for pointing */
  int N_stars;      /* Number of stars in model sample */
  double * Z;       /* array of star heights above gal plane */
  double * R;       /* array of star distances from gal center in gal plane */
  double * weight;  /* star's density weight based on Z, R */
  RBIN * rbin;      /* Nbins of these structures */
  //COV * cov_row;    /* Covariance matrix: first index is a row */
  //COR * cor_row;    /* Correlation matrix: first index is a row */
  INVCOV * invcov_row; /* Inverted covariance matrix: first index is a row */
} POINTING;

/* Data for each step in MCMC chain */
typedef struct {
  double thin_r0;           /* thin disk scale length */
  double thin_z0;           /* thin disk scale height */
  double thick_r0;          /* thick disk scale length */
  double thick_z0;          /* thick disk scale height */
  double ratio_thick_thin;  /* number density ratio */
  double chi2;              /* total chi2 for step */
  double chi2_reduced;      /* chi2/DOF */
} STEP_DATA;

/* I/O functions */
void load_pointingID(int *N_plist, POINTING **plist);
int load_Nbins(void);
void load_ZRW(POINTING *plist, int lower_ind, int upper_ind, int rank);
void load_rbins(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank);
void load_pairs(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank);
// void load_covariance(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank);
// void load_correlation(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank);
void load_inv_covariance(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank);
void load_step_data(STEP_DATA *step_data, int flag, int rank);
void output_mcmc(int index, STEP_DATA p, FILE *output_file);

/* Stats functions */
// void calculate_frac_error(POINTING *p, int N_bins, int lower_ind, int upper_ind);
double calculate_chi2(POINTING *p, int N_bins, int lower_ind, int upper_ind);

/* MCMC functions */
void set_weights(STEP_DATA params, POINTING *p, int lower_ind, int upper_ind);
double normalize_MM(double *weight, int N_stars);
double calculate_MM( unsigned int N_pairs, int *pair1, int *pair2, double MM_norm,
  double *weight );
void calculate_DD_RR(POINTING *p, int N_bins, int lower_ind, int upper_ind);
void calculate_correlation(POINTING *p, int N_bins, int lower_ind, int upper_ind);
int degrees_of_freedom(POINTING *p, int N_bins, int lower_ind, int upper_ind);
STEP_DATA update_parameters(STEP_DATA p, gsl_rng * GSL_r);
void run_mcmc(POINTING *plist, STEP_DATA initial, int N_bins, int max_steps,
    int lower_ind, int upper_ind, int rank, int nprocs, char *file_string[256]);

/* Other */
double sech2(double x);