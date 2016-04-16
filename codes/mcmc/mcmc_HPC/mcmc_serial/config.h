#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <string.h>


/* Set the value of pi */
#define PI 3.14159265358979323846

#define DATA_DIR "../data/"
#define TMP_DATA_DIR "./tmpdata/"

/* A structure for a point */
typedef struct STAR{
  double ra_rad, dec_rad, distance;
  double galactic_l_rad, galactic_b_rad;
  double galactic_Z, galactic_R;
  double x, y, z;
  double weight;
} STAR;

/* A holder for correlations */
typedef struct CORRELATION{
  double r_lower, r_upper, r_middle, bin_size;
  double r2_lower, r2_upper;
  long DD_N, MM_N;		/* raw number of pairs without weighting */
  double DD, MM;		/* weighted and normalized pair counts */
  double correlation;

  /* errors */
  double sigma2_dd, sigma2_mm;	/* sigma square for weighted DD and MM */
  double sigma2_dd_n, sigma2_mm_n;	/* sigma square for raw pairs DD_N and MM_N */
  double sigma, sigma2, chi2;		/* variances and chi square of correlations */
  double err_jk_dd, err_jk_mm;		/* fractional error calculated from jackknife samples */

} CORRELATION;


/* correlation function range and bins */
extern double CORR_R_MIN;
extern double CORR_R_MAX;
extern int N_BINS;


/* A structure for a plate pointing to the sky */
typedef struct POINTING{
  char ID[256];
  double ra_deg, dec_deg, ra_rad, dec_rad;
  double galactic_l_rad, galactic_b_rad;
  double x, y, z;	/* Cartesians on unit sphere */
  double r_min, r_max;		/* distances range */
  int N_data;
  STAR *data;
  int N_model;
  STAR *model;
  int N_corr;
  CORRELATION *corr;
} POINTING;


/* A structure for parameters of model.*/
typedef struct PARAMETERS{

  /* Use a mode number to set different scenario */
  int Mode;

  /* Total number of free paramters */
  /* Set this carefully! Otherwise the DOF will be wrong. */
  int N_parameters;

  /* thin disk parameters */
  int thindisk_type;		
  double thindisk_r0; 		/* thin disk scale length */
  double thindisk_z0;		/* thin disk scale height */
  double thindisk_n0;		/* normalization factor */

  /* thick disk parameters */
  int thickdisk_type;
  double thickdisk_r0;		/* thick disk scale length */
  double thickdisk_z0;		/* thick disk scale height */
  double thickdisk_n0;		/* normalization factor */

  /* The ratio of n0 between thickdisk_n0 and thin_disk_n0. */
  /* While doing two-disk model, only the ratio matters. */
  double n0_ratio_thick_thin;

  /* halo parameters */
  int halo_type;
  double halo_scaleradius;
  double halo_innerslope;
  double halo_n0;		/* normalization factor */

  /* sun's position */
  int sun_position;
  double sun_R; 		/* sun's distance away from Galactic center */
  double sun_Z;			/* sun's height from Galactic plane */

} PARAMETERS;



/* A structure for elements in Markov chain */
typedef struct MCMC {
  PARAMETERS params;
  double chi2, dof, chi2_reduced;
} MCMC;


/* A holder for a vector in Cartesian coordinates */
typedef struct VECTOR{
  double x, y, z;
} VECTOR;





/* function names */

/* io functions */
void load_parameters(PARAMETERS *params);
void load_pointing_list(int *N_plist, POINTING **plist);
void load_data(int N_plist, POINTING *plist);
void load_model(int N_plist, POINTING *plist);
CORRELATION * load_rbins(char *bins_filename, int *N_rbins);


/* Galaxy model functions */
void set_weights(PARAMETERS params, POINTING *plist, int N_plist);
double total_density(PARAMETERS p, double r, double z);


/* correlation calculation functions */
void pairs_los_data(POINTING *p);
void pairs_los_model(POINTING *p);
void correlation_los(POINTING *p);
void correlation_initialize(POINTING *plist, int N_plist);
void calculate_correlation(POINTING *plist, int N_plist);
void correlation_average(POINTING *plist, int N_plist);

/* MCMC functions */
void load_errors(int N_plist, POINTING *plist);
int degrees_of_freedom(POINTING *plist, int N_plist, PARAMETERS params);
double chi_square(POINTING *plist, int N_plist);
PARAMETERS update_parameters(PARAMETERS p);
void output_mcmc(int index, MCMC current, FILE *output_file);
void run_mcmc(PARAMETERS initial_params, int max_steps, int N_plist, POINTING *plist);


/* misc functions */
double sech2(double x);
void eq2cart(STAR *s);
void cart2eq(STAR *s);
void eq2gal(STAR *s);
void gal2eq(STAR *s);
void gal2ZR(STAR *s, PARAMETERS params);
