/* Functions for MCMC calculation */

#include "config.h"

#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_integration.h>


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

      //fprintf(stderr, "%lf\t%lf\n", sigma2_dd, sigma2_mm);

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

  double n0_ratio_thick_thin_sigma;
  n0_ratio_thick_thin_sigma = 0.002;

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
    delta = gsl_ran_gaussian(GSL_r, n0_ratio_thick_thin_sigma);
    p.n0_ratio_thick_thin += delta;
    if(p.n0_ratio_thick_thin < 1.0) break;
  }
  p.thickdisk_n0 = p.thindisk_n0 * p.n0_ratio_thick_thin;

  return p;
}


void output_mcmc(int index, MCMC current, FILE *output_file){

  /* output mcmc chain element */
  PARAMETERS p;
  p = current.params;

  if(p.N_parameters == 2){
    fprintf(output_file, "%d\t%lf\t%lf\t%lf\t%lf\t%lf\n",
	    index, current.dof, current.chi2, current.chi2/current.dof,
	    p.thindisk_r0, p.thindisk_z0);
  }
  else if(p.N_parameters == 5){
    fprintf(output_file, "%d\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\n",
	    index, current.dof, current.chi2, current.chi2/current.dof,
	    p.thindisk_r0, p.thindisk_z0,
	    p.thickdisk_r0, p.thickdisk_z0, p.n0_ratio_thick_thin
	    );
  }

}


void run_mcmc(PARAMETERS initial_params, int max_steps, int N_plist, POINTING *plist){

  int i, efficiency_counter;
  double efficiency;
  MCMC current, new;
  double delta_chi2;

  fprintf(stderr, "Start MCMC chain..Max steps = %d \n", max_steps);

  /* set the first element as the initial parameters.
   Then calculate the chi2 for the initial parameters. */
  current.params = initial_params;

  /* set initial weights */
  set_weights(current.params, plist, N_plist);

  /* allocate space for correlation function calculation */
  /* This also does a first time correlation calculation of initial parameters. */
  /* DD pairs may only be calculated once here but not later.  */
  fprintf(stderr, "corr initial\n");

  current.dof = degrees_of_freedom(plist, N_plist, current.params);
  current.chi2 = chi_square(plist, N_plist);

  fprintf(stderr, "initial: chi2 = %le \n", current.chi2);

  /* result output to */
  char output_filename[256];
  FILE *output_file;
  snprintf(output_filename, 256, "%smcmc_result.dat", DATA_DIR);
  output_file = fopen(output_filename, "a");


  /* Markov chain loop */
  efficiency_counter = 1;
  for(i = 1; i < max_steps; i++){

    /* update new positions in paramter space */
    new.params = update_parameters(current.params);

    /* recalculate weights */
    set_weights(new.params, plist, N_plist);

    /* recalculate correlation functions */
    calculate_correlation(plist, N_plist);

    /* get chi squares */
    new.dof = degrees_of_freedom(plist, N_plist, new.params);

    new.chi2 = chi_square(plist, N_plist);

    delta_chi2 = new.chi2 - current.chi2;

    if(delta_chi2 <= 0.0){
      /* if delta chisquare is smaller then record*/
      current = new;
      efficiency_counter++;
    }
    else{
      /* if delta chisquare is bigger then use probability to decide */
      /* !!! replace with GSL random generator later !!! */
      double tmp = (double)rand() / (double)RAND_MAX; /* a random number in [0,1] */
      if (tmp < exp(- delta_chi2 / 2.0)){
	current = new;
	efficiency_counter++;
      }
      else{
	/* use the old position. */
      }
    }

    output_mcmc(i, current, output_file);

    if(i % 50 == 0){
      fflush(output_file);
    }

    efficiency = (float) efficiency_counter / i;
    /* print out progress */
    /* if(i % (max_steps / 100) == 0){ */
    /*   fprintf(stderr, "MCMC... %d / %d: chi2 = %lf \n", i, max_steps, new.chi2); */
    /* } */
    fprintf(stderr, "MCMC... %d / %d: efficiency = %lf, delta_chi2 = %le \n",
	    i, max_steps, efficiency, delta_chi2);

    fprintf(stderr,
	    "\t Trying: z0_thin = %lf, r0_thin = %lf, z0_thick = %lf, r0_thick = %lf, n0_thick = %lf \n",
	    new.params.thindisk_z0, new.params.thindisk_r0,
	    new.params.thickdisk_z0, new.params.thickdisk_r0, new.params.n0_ratio_thick_thin);
    fprintf(stderr,
	    "\t Current: delta_chi2 = %le, chi2 = %lf, dof = %lf, chi2_reduced = %lf \n\n",
	    delta_chi2, new.chi2, new.dof, new.chi2/new.dof);

  }


  fclose(output_file);

  fprintf(stderr, "MCMC result output to %s\n", output_filename);
  fprintf(stderr, "End MCMC calculation..\n");

}
