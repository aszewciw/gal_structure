#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>
#include <math.h>
#include <time.h>
#include <string.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_integration.h>
#include <omp.h>

/* I/O directories */
#define RAW_DIR "../../../data/"
#define DATA_DIR "../data/"
#define DD_DIR "../data/mock_dd/"
#define ERR_DIR "../data/errors/"
#define OUT_DIR "../data/mcmc_output/"
#define PAIRS_DIR "../data/model_pairs/"
#define ZR_DIR "../../prepare_randoms/data/"


/* Data for each radial bin */
typedef struct {
  char binID[256];      // ID for each radial bin
  double DD;            // segue pair counts
  double MM;            // model pair counts
  double corr;          // DD/MM
  double DD_err_jk;     // fractional segue jk error
  double MM_err_jk;     // fractional model jk error
  double err2_frac;     // fractional errors squared
  double sigma2;        // sigma squared for DD/MM
  unsigned int N_pairs; // number of unique pairs
  int * pair1;          // array of pair1 index of length N_pairs
  int * pair2;          // array of pair2 index of length N_pairs
} RBIN;

/* A structure to store data for the weighted uniform stars */
typedef struct {
  int N_stars;      // Number of stars in model sample
  double * Z;       // array of star heights above gal plane
  double * R;       // array of star distances from gal center in gal plane
  double * weight;  // star's density weight based on Z, R
  RBIN * rbin;      // Nbins of these; Nbins should be global or declared in main
} MODEL;

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
void load_ZR(MODEL *m);
void load_rbins(MODEL *m, int N_bins);
void load_pairs(MODEL *m, int N_bins);
void load_step_data(STEP_DATA *step_data);
void output_mcmc(int index, STEP_DATA p, FILE *output_file);

/* Stats functions */
void calculate_frac_error(MODEL *m, int N_bins);
double calculate_chi2(MODEL *m, int N_bins);

/* MCMC functions */
void set_weights(STEP_DATA params, MODEL *m);
double normalize_MM(double *weight, int N_stars);
double calculate_MM( unsigned int N_pairs, int *pair1, int *pair2, double MM_norm, double *weight );
void calculate_correlation(MODEL *m, int N_bins);
int degrees_of_freedom(MODEL *m, int N_bins);
STEP_DATA update_parameters(STEP_DATA p, gsl_rng * GSL_r);
void run_mcmc(MODEL *model, STEP_DATA initial, int N_bins, int max_steps);

/* Other */
double sech2(double x);