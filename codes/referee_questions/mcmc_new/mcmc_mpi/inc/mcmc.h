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
  double r0_thin;     /* thin disk scale length */
  double z0_thin;     /* thin disk scale height */
  double r0_thick;    /* thick disk scale length */
  double z0_thick;    /* thick disk scale height */
  double ratio;       /* thick:thin number density ratio */
  char filename[256]; /* name of output file */
  int max_steps;      /* max steps in MCMC chain */
} ARGS;

/* Data for each radial bin */
typedef struct {
  char binID[256];      /* ID for each radial bin */
  double DD;            /* segue pair counts */
  double MM;            /* model pair counts */
  // double RR;            /* uniform pair counts */
  double frac_error;    /* fractional error in model */
  double sigma2;        /* sigma squared for MM/RR */
  unsigned int N_pairs; /* number of unique pairs */
  int * pair1;          /* array of pair1 index of length N_pairs */
  int * pair2;          /* array of pair2 index of length N_pairs */
} RBIN;

/* Pointing line of sight in sky */
typedef struct {
  char ID[256];     /* Unique ID for pointing */
  int N_stars;      /* Number of stars in model sample */
  double * Z;       /* array of star heights above gal plane */
  double * R;       /* array of star distances from gal center in gal plane */
  double * weight;  /* star's density weight based on Z, R */
  RBIN * rbin;      /* Nbins of these structures */
} POINTING;

/* Data for each step in MCMC chain */
typedef struct {
  double r0_thin;           /* thin disk scale length */
  double z0_thin;           /* thin disk scale height */
  double r0_thick;          /* thick disk scale length */
  double z0_thick;          /* thick disk scale height */
  double ratio_thick_thin;  /* number density ratio */
  double chi2;              /* total chi2 for step */
  double chi2_reduced;      /* chi2/DOF */
} STEP_DATA;

/* I/O functions */
ARGS parse_command_line( int n_args, char ** arg_array );
void load_pointingID(int *N_plist, POINTING **plist);
int load_Nbins(void);
void load_ZRW(POINTING *plist, int lower_ind, int upper_ind, int rank);
void load_rbins(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank);
void load_pairs(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank);
// void load_step_data(STEP_DATA *step_data, int flag, int rank);
void output_mcmc(int index, STEP_DATA p, FILE *output_file);

/* Stats functions */
double calculate_chi2(POINTING *p, int N_bins, int lower_ind, int upper_ind);

/* MCMC functions */
void set_weights(STEP_DATA params, POINTING *p, int lower_ind, int upper_ind);
double normalize_MM(double *weight, int N_stars);
double calculate_MM( unsigned int N_pairs, int *pair1, int *pair2, double MM_norm,
  double *weight );
void update_model(POINTING *p, int N_bins, int lower_ind, int upper_ind);
// void calculate_correlation(POINTING *p, int N_bins, int lower_ind, int upper_ind);
int degrees_of_freedom(POINTING *p, int N_bins, int lower_ind, int upper_ind);
STEP_DATA update_parameters(STEP_DATA p, gsl_rng * GSL_r);
void run_mcmc(POINTING *plist, int N_params, STEP_DATA initial, int N_bins, int max_steps,
    int lower_ind, int upper_ind, int rank, int nprocs, char filename[256]);

/* Other */
double sech2(double x);