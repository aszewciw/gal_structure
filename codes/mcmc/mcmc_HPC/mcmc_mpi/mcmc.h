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

/* Set the value of pi */
#define PI 3.14159265358979323846

#define DATA_DIR "../data/"
#define DD_DIR "../data/dd/"
#define ERR_DIR "../data/errors/"
#define OUT_DIR "../data/mcmc_output/"
#define PAIRS_DIR "../data/model_pairs/"
#define ZRW_DIR "../data/model_positions/"
#define RAW_DIR "../data/raw/"


/* Data for each radial bin */
typedef struct {
  char binID[256]; // ID for each radial bin
  double DD; // segue pair counts
  double MM; // model pair counts
  double corr; // DD/MM
  double DD_err_jk; // fractional segue jk error
  double MM_err_jk; // fractional model jk error
  double err2_frac; // fractional errors squared
  double sigma2; // sigma squared for DD/MM
  unsigned int N_pairs; // number of unique pairs
  int * pair1; // array of pair1 index of length N_pairs
  int * pair2; // array of pair2 index of length N_pairs
} RBIN;

/* Pointing line of sight in sky */
typedef struct {
  char ID[256]; // Unique ID for pointing
  int N_stars; //Number of stars in model sample
  double * Z; // array of star heights above gal plane
  double * R; // array of star distances from gal center in gal plane
  double * weight; // star's density weight based on Z, R
  RBIN * rbin; // Nbins of these; Nbins should be global or declared in main
} POINTING;


/* Data for each step in MCMC chain */
typedef struct {
  double thin_r0; /* thin disk scale length */
  double thin_z0; /* thin disk scale height */
  double thick_r0; /* thick disk scale length */
  double thick_z0; /* thick disk scale height */
  double ratio_thick_thin; /* number density ratio */
  double chi2; /* total chi2 for step */
  double chi2_reduced; /* chi2/DOF */
} STEP_DATA;

/* I/O functions */
void load_pointingID(int *N_plist, POINTING **plist);
void load_ZRW(POINTING *plist, int lower_ind, int upper_ind, int rank);
void load_rbins(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank);
void load_pairs(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank);
void load_step_data(STEP_DATA *step_data);

/* Error functions */
void calculate_frac_error(POINTING *p, int N_bins, int lower_ind, int upper_ind);
double calculate_chi2(POINTING *p, int N_bins, int lower_ind, int upper_ind);

/* MCMC functions */
void set_weights(STEP_DATA params, POINTING *p, int lower_ind, int upper_ind);
double normalize_MM(double *weight, int N_stars);
double calculate_MM( unsigned int N_pairs, int *pair1, int *pair2, double MM_norm, double *weight );
void calculate_correlation(POINTING *p, int N_bins, int lower_ind, int upper_ind);
int degrees_of_freedom(POINTING *p, int N_bins, int lower_ind, int upper_ind);
STEP_DATA update_parameters(STEP_DATA p, gsl_rng * GSL_r);
void run_mcmc(POINTING *plist, STEP_DATA initial, int N_bins, int max_steps,
    int lower_ind, int upper_ind, int rank, int nprocs);
void output_mcmc(int index, STEP_DATA p, FILE *output_file);

/* Other */
double sech2(double x);