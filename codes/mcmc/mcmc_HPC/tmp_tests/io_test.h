#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <string.h>


/* Set the value of pi */
#define PI 3.14159265358979323846

#define DATA_DIR "../data/"
#define DD_DIR "../data/dd/"
#define ERR_DIR "../data/errors/"
#define OUT_DIR "../data/mcmc_output/"
#define PAIRS_DIR "../data/model_pairs/"
#define ZRW_DIR "../data/model_positions/"
#define RAW_DIR "../data/raw/"


// Data for each radial bin
typedef struct {
  char binID[256]; // ID for each radial bin
  float DD; // segue pair counts
  float MM; // model pair counts
  float corr; // DD/MM
  float DD_err_jk; // fractional segue jk error
  float MM_err_jk; // fractional model jk error
  float err2_frac; // fractional errors squared
  float sigma2; // sigma squared for DD/MM
  unsigned int N_pairs; // number of unique pairs
  unsigned int * pair1; // array of pair1 index of length N_pairs
  unsigned int * pair2; // array of pair2 index of length N_pairs
} RBIN;

// Pointing line of sight in sky
typedef struct {
  char ID[256]; // Unique ID for pointing
  int N_stars; //Number of stars in model sample
  float * Z; // array of star heights above gal plane
  float * R; // array of star distances from gal center in gal plane
  float * weight; // star's density weight based on Z, R
  RBIN * rbin; // Nbins of these; Nbins should be global or declared in main
} POINTING;

/* function names */
void load_pointingID(int *N_plist, POINTING **plist);
void load_ZRW(int N_plist, POINTING *plist);
void load_rbins(int N_plist, int N_bins, POINTING *plist);
void load_pairs(int N_plist, int N_bins, POINTING *plist);


