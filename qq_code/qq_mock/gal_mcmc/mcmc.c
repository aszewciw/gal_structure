/* Functions for MCMC calculation */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_integration.h>

#include "config.h"

void load_errors(POINTING *plist, int N_plist){

  int i, k;

  char data_dir[256];
  snprintf(data_dir, 256, "../data/");

  for(i = 0; i < N_plist; i++){
    char data_error_filename[256];
    char model_error_filename[256];
    snprintf(data_error_filename, 256, "%sstar_%s_jk_error.dat", data_dir, plist[i].ID);
    snprintf(model_error_filename, 256, "%suniform_%s_jk_error.dat", data_dir, plist[i].ID);

    FILE *data_error_file, *model_error_file;
    
    if((data_error_file=fopen(data_error_filename,"r"))==NULL){
      fprintf(stderr,"Error: Cannot open file %s \n", data_error_filename);
      exit(EXIT_FAILURE);
    }

    for(k = 0; k < plist[i].N_corr; k++){
      double r_lower, r_upper, r_middle, bin_size, tmp;
      fscanf(data_error_file, "%lf", &r_lower);
      fscanf(data_error_file, "%lf", &r_upper);
      fscanf(data_error_file, "%lf", &r_middle);
      fscanf(data_error_file, "%lf", &bin_size);
      fscanf(data_error_file, "%lf", &tmp);
      fscanf(data_error_file, "%lf", &tmp);
      fscanf(data_error_file, "%lf", &tmp);
      fscanf(data_error_file, "%lf", &plist[i].corr[k].err_jk_dd);
    }

    if((model_error_file=fopen(model_error_filename,"r"))==NULL){
      fprintf(stderr,"Error: Cannot open file %s \n", model_error_filename);
      exit(EXIT_FAILURE);
    }

    for(k = 0; k < plist[i].N_corr; k++){
      double r_lower, r_upper, r_middle, bin_size, tmp;
      fscanf(model_error_file, "%lf", &r_lower);
      fscanf(model_error_file, "%lf", &r_upper);
      fscanf(model_error_file, "%lf", &r_middle);
      fscanf(model_error_file, "%lf", &bin_size);
      fscanf(model_error_file, "%lf", &tmp);
      fscanf(model_error_file, "%lf", &tmp);
      fscanf(model_error_file, "%lf", &tmp);
      fscanf(model_error_file, "%lf", &plist[i].corr[k].err_jk_mm);
    }

  } 

  fprintf(stderr, "Jackknife errors successfully loaded. \n");

}


int degrees_of_freedom(POINTING *plist, int N_plist, PARAMETERS params){

  int i, k;
  int dof = 0;

  POINTING *p;

  /* loop over all line of sight */
  for(i = 0; i < N_plist; i++){

    p = &plist[i];

    for(k = 0; k < p->N_corr; k++){

      if(p->corr[k].MM_N == 0){
	/* fprintf(stderr, "Warning: The number density of the model points is too low. \n"); */
	continue;
      }

      if(p->corr[k].DD_N == 0){
	/* fprintf(stderr, "Warning: Skip empty bin [%lf, %lf] in pointing %s . \n",  */
	/* 	p->corr[k].r_lower, p->corr[k].r_upper, p->ID); */
	continue;
      }

      /* only count bins with non zero pairs. */
      dof++;
    }

  }

  dof = dof - params.N_parameters;

  return dof;
}


double chi_square(POINTING *plist, int N_plist){

  int i, k;
  double sigma2_dd, sigma2_mm, sigma2, chi2;
  double dd, mm;
  long dd_n, mm_n;

  POINTING *p;

  chi2 = 0.0;

  /* loop over all line of sight */
  for(i = 0; i < N_plist; i++){

    p = &plist[i];

    for(k = 0; k < p->N_corr; k++){

      /* use raw pair counting without weights to calcuate a fractional error. 
	 Then use this fraction to calcuate the error of weighted counting. 
	 sigma = sqrt(N_raw)/N_raw * N_weighted */

      /* Skip bins with zero pairs, otherwise division by zero may occur! */
      /* This should be consistent with degrees of freedom calculation. */

      dd_n = p->corr[k].DD_N;
      if(dd_n == 0){
	continue;
      }

      mm_n = p->corr[k].MM_N;
      if(mm_n == 0){
	continue;
      }

      dd = p->corr[k].DD;
      //sigma2_dd = (1.0 / (double)dd_n) * dd * dd;
      sigma2_dd = (p->corr[k].err_jk_dd * dd) * (p->corr[k].err_jk_dd * dd);

      mm = p->corr[k].MM;
      //sigma2_mm = (1.0 / (double)mm_n) * mm * mm;
      sigma2_mm = (p->corr[k].err_jk_mm * mm) * (p->corr[k].err_jk_mm * mm);

      /* ignore tidy errors which may be caused by 0 jackknife error */
      if(sigma2_dd == 0.0 || sigma2_mm == 0.0){
        continue;
      }

      /* propagate to get the total error of dd/mm */
      /* sigma2/f^2 = sigma2_dd/dd^2 + sigma2_mm/mm^2  */
      /* note sigma2 is the error square of dd/mm */
      double f = dd / mm; 
      sigma2 = (sigma2_dd / (dd * dd) + sigma2_mm / (mm * mm)) * (f * f);
      
      /* The expected dd/mm is 1 */
      chi2 += (f - 1.0) * (f - 1.0) / sigma2;

      p->corr[k].sigma2_dd = sigma2_dd;
      p->corr[k].sigma2_mm = sigma2_mm;
      p->corr[k].sigma2 = sigma2;
      p->corr[k].chi2 = (f - 1.0) * (f - 1.0) / sigma2;

    }
  }


  return chi2;

}


PARAMETERS update_parameters(PARAMETERS p){

  double delta;

  /* variance for each parameter, only used for initialization. */
  double thindisk_z0_sigma, thindisk_r0_sigma;
  thindisk_z0_sigma = 0.005;
  thindisk_r0_sigma = 0.05;

  double thickdisk_z0_sigma, thickdisk_r0_sigma;
  thickdisk_z0_sigma = 0.005;
  thickdisk_r0_sigma = 0.05;
  
  double thickdisk_n0_sigma;
  thickdisk_n0_sigma = 0.002;

  /* use gsl library to get Gaussian random numbers. */
  const gsl_rng_type * GSL_T;
  gsl_rng * GSL_r;

  gsl_rng_env_setup();

  GSL_T = gsl_rng_default;
  GSL_r = gsl_rng_alloc(GSL_T);

  gsl_rng_set(GSL_r, time(NULL));

  /* change the position based on Gaussian distributions.  */
  delta = gsl_ran_gaussian(GSL_r, thindisk_z0_sigma);
  p.thindisk_z0 = p.thindisk_z0 + delta;

  delta = gsl_ran_gaussian(GSL_r, thindisk_r0_sigma);
  p.thindisk_r0 = p.thindisk_r0 + delta;

  delta = gsl_ran_gaussian(GSL_r, thickdisk_z0_sigma);
  p.thickdisk_z0 = p.thickdisk_z0 + delta;

  delta = gsl_ran_gaussian(GSL_r, thickdisk_r0_sigma);
  p.thickdisk_r0 = p.thickdisk_r0 + delta;

  while(1){
    delta = gsl_ran_gaussian(GSL_r, thickdisk_n0_sigma);
    p.thickdisk_n0 = p.thickdisk_n0 + delta;
    if(p.thickdisk_n0 < 1.0) break;
  }

  return p; 
}


void output_mcmc(MCMC *mcmc_chain, int mcmc_steps){
  
  /* output mcmc chain */
 
  char output_filename[256];
  FILE *output_file;

  snprintf(output_filename, 256, "./data/mcmc.dat");

  output_file = fopen(output_filename, "w");

  int i;
  for(i = 0; i < mcmc_steps; i++){
    double r0_thin, z0_thin, r0_thick, z0_thick, n0_thick, chi2, chi2_reduced;
    int dof;
    r0_thin = mcmc_chain[i].params.thindisk_r0;
    z0_thin = mcmc_chain[i].params.thindisk_z0;
    r0_thick = mcmc_chain[i].params.thickdisk_r0;
    z0_thick = mcmc_chain[i].params.thickdisk_z0;
    n0_thick = mcmc_chain[i].params.thickdisk_n0;
    chi2 = mcmc_chain[i].chi2; 
    dof = mcmc_chain[i].dof; 
    chi2_reduced = chi2 / dof;

    fprintf(output_file, "%d\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%d\t%lf\n",
	    i, r0_thin, z0_thin, r0_thick, z0_thick, n0_thick, chi2, dof, chi2_reduced);
  }

  fprintf(stderr, "MCMC result output to %s\n", output_filename);
  
  fclose(output_file);

}
