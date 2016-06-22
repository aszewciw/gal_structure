#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>
#include <math.h>
#include <time.h>
#include <string.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_integration.h>

/* I/O directories */
#define RAW_DIR     "../../../data/"
#define DATA_DIR    "../data/"
#define BIN_DIR     "../data/rbins/"
#define DENSITY_DIR "../data/mock_density/"
#define ZR_DIR      "../data/model_positions/"
#define OUT_DIR     "../data/mcmc_output/"


/* Data for each radial bin */
typedef struct {
  char binID[256];          // ID for each radial bin
  double N_mock;            // raw counts in bin
  double N_mock_err;        // sqrt(N) Poisson error
  double density_mock;      // Npoints/volume
  double density_mock_err;  // propagated error in density
  double sigma2;            // err**2 for use in chi2 calculation
  double N_uniform;         // number of uniform stars in bin
  double * Z;               // height above plane of stars
  double * R;               // distance from Z axis of star
  double * density;         // density value, based on Z,R
  double average_density;   // Average density value in bin
} RBIN;

/* Pointing line of sight in sky */
typedef struct {
  char ID[256]; // Unique ID for pointing
  RBIN * rbin;  // Nbins of these; Nbins should be global or declared in main
} POINTING;

// typedef struct {
//   double *r_inner;  /* array of inner distance */
//   double *r_outer;   array of outer distance
//   double *volume;   /* array of bin volumes */
// } BIN_INFO;

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
void load_bin_info(int *N_bins);
void load_mock_data(int N_p, POINTING *p, int N_bins);
void load_ZR(int N_p, POINTING *p, int N_bins);
void load_step_data(STEP_DATA *step_data);
void output_mcmc(int index, STEP_DATA p, FILE *output_file);

// /* Stats functions */
// void calculate_frac_error(POINTING *p, int N_bins, int lower_ind, int upper_ind);
// double calculate_chi2(POINTING *p, int N_bins, int lower_ind, int upper_ind);

// /* MCMC functions */
// void set_weights(STEP_DATA params, POINTING *p, int lower_ind, int upper_ind);
// double normalize_MM(double *weight, int N_stars);
// double calculate_MM( unsigned int N_pairs, int *pair1, int *pair2, double MM_norm, double *weight );
// void calculate_correlation(POINTING *p, int N_bins, int lower_ind, int upper_ind);
// int degrees_of_freedom(POINTING *p, int N_bins, int lower_ind, int upper_ind);
// STEP_DATA update_parameters(STEP_DATA p, gsl_rng * GSL_r);
// void run_mcmc(POINTING *plist, STEP_DATA initial, int N_bins, int max_steps,
//     int lower_ind, int upper_ind, int rank, int nprocs);

// /* Other */
// double sech2(double x);