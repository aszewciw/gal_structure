/* 
   Functions for calculate the correlation functions 
   between data and random catalog.
*/

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <omp.h>

#include "config.h"


double CORR_R_MIN = 0.005;
double CORR_R_MAX = 2.0;
int N_BINS = 12;


/* ------------------------------------------------------------------------- */
/* Calculate the total number of pairs available, for normalization purpose. */
double pairs_norm(STAR *data, int N_data){
  
  double total = 0.0;
  int i, j;
  
  for(i = 0; i < N_data; i++){
    for(j = i + 1; j < N_data; j++){
      total += data[i].weight * data[j].weight;
    }
  }
  
  return total;
}

/* ------------------------------------------------------------------------- */
/* counting pairs in data for one line of sight */
void pairs_los_data(POINTING *p){


  int i, j, k;

  for(i = 0; i < p->N_corr; i++){
    p->corr[i].DD_N = 0;
    p->corr[i].DD = 0.0;
  }

  // calculate the correlation
  /* fprintf(stderr, "Start calculating the correlation function... \n"); */
  double DD_norm;
  DD_norm = pairs_norm(p->data, p->N_data);

  double dx, dy, dz, ds, r1, r2;

  /* counting pairs for data */
  for(i = 0; i < p->N_data; i++){
    for(j = i + 1; j < p->N_data; j++){

      dx = p->data[i].x - p->data[j].x;
      dy = p->data[i].y - p->data[j].y;
      dz = p->data[i].z - p->data[j].z;

      //ds = sqrt(dx * dx + dy * dy + dz * dz); /* distance */
      ds = dx * dx + dy * dy + dz * dz; /* distance */

      for(k = 0; k < p->N_corr; k++){
	r1 = p->corr[k].r2_lower;
	r2 = p->corr[k].r2_upper;
	if(ds >= r1 && ds < r2){
	  p->corr[k].DD_N += 1;
	  p->corr[k].DD += p->data[i].weight * p->data[j].weight;
	  break;
	}
      }
    
    }
  }
  
  for(k = 0; k < p->N_corr; k++){
    /* normalize all the values */
    p->corr[k].DD /= DD_norm;
  }

}

/* ------------------------------------------------------------------------- */
/* counting pairs in model for one line of sight */
void pairs_los_model(POINTING *p){

  int i, j, k;

  for(i = 0; i < p->N_corr; i++){
    p->corr[i].MM_N = 0;   
    p->corr[i].MM = 0.0;
  }

  // calculate the correlation
  /* fprintf(stderr, "Start calculating the correlation function... \n"); */
  double MM_norm;
  MM_norm = pairs_norm(p->model, p->N_model);
  
  double dx, dy, dz, ds, r1, r2;

  /* counting pairs for model */
  for(i = 0; i < p->N_model; i++){
    for(j = i + 1; j < p->N_model; j++){

      dx = p->model[i].x - p->model[j].x;
      dy = p->model[i].y - p->model[j].y;
      dz = p->model[i].z - p->model[j].z;

      //ds = sqrt(dx * dx + dy * dy + dz * dz); /* distance */
      ds = dx * dx + dy * dy + dz * dz; /* distance */

      for(k = 0; k < p->N_corr; k++){
	r1 = p->corr[k].r2_lower;
	r2 = p->corr[k].r2_upper;
	if(ds >= r1 && ds < r2){
	  p->corr[k].MM_N += 1;
	  p->corr[k].MM += p->model[i].weight * p->model[j].weight;
	  break;
	}
      }
    
    }
  }
  
  for(k = 0; k < p->N_corr; k++){
    /* normalize all the values */
    p->corr[k].MM /= MM_norm;
  }

}


/* ------------------------------------------------------------------------- */
/* calculate correlations for one line of sight */
void correlation_los(POINTING *p){
  
  int k;
  /* calculate correlations */
  for(k = 0; k < p->N_corr; k++){
    p->corr[k].correlation = p->corr[k].DD / p->corr[k].MM - 1.0 ;
  }

}


/* allocate space for correlation function calculation */
/* This also does a first time correlation calculation of initial parameters. */
/* DD pairs may only calculated once here but not later.  */
void correlation_initialize(POINTING *plist, int N_plist){

  /* initialize the r range for each bin */
  double corr_rmax_log, corr_rmin_log, corr_dr_log;
  corr_rmax_log = log10(CORR_R_MAX);
  corr_rmin_log = log10(CORR_R_MIN);
  corr_dr_log = (corr_rmax_log - corr_rmin_log) / N_BINS;

  int i, k;

  for(i = 0; i < N_plist; i++){

    POINTING *p;
    p = &plist[i];

    /* allocate memory for each line of sight */
    p->N_corr = N_BINS;
    p->corr = calloc(p->N_corr, sizeof(CORRELATION));

    for(k = 0; k < p->N_corr; k++){
      p->corr[k].r_lower = pow(10.0, corr_rmin_log + k * corr_dr_log);
      p->corr[k].r_upper = pow(10.0, corr_rmin_log + (k + 1) * corr_dr_log);
      p->corr[k].r_middle = pow(10.0, corr_rmin_log + (k + 0.5) * corr_dr_log);
      p->corr[k].r2_lower = p->corr[k].r_lower * p->corr[k].r_lower;
      p->corr[k].r2_upper = p->corr[k].r_upper * p->corr[k].r_upper;
      p->corr[k].DD_N = 0;
      p->corr[k].MM_N = 0;   
      p->corr[k].DD = 0.0;
      p->corr[k].MM = 0.0;
      p->corr[k].correlation = 0.0;
    }

    /* data pairs may only be updated here once, but not later. */
    /* check with causion. */
    pairs_los_data(p);

    pairs_los_model(p);

    correlation_los(p);

  }

}


/* ------------------------------------------------------------------------- */
/* A wrapper to loop over all lines of sight */
void calculate_correlation(POINTING *plist, int N_plist){
  int i;

  # pragma omp parallel for schedule(dynamic) 
  /* calculate correlation functions for all pointings.*/
  for(i = 0; i < N_plist; i++){
    //for(i = 0; i < 1; i++){

    /* if(i % (N_plist / 20) == 0) */
    /*   fprintf(stderr, "Calculating correlation: %d of %d pointings..\n", i, N_plist); */

    /* data pairs do not need to be updated every time */
    /* disable with causion. */
    /* pairs_los_data(&plist[i]); */

    pairs_los_model(&plist[i]);

    correlation_los(&plist[i]);

    /* char output_filename[256]; */
    /* FILE *output_file; */
    /* snprintf(output_filename, 256, "./tmp/corr_%s.tmp.dat", plist[i].ID); */
    /* output_file = fopen(output_filename, "w"); */
    /* for(j = 0; j < plist[i].N_corr; j++){ */
    /*   double r1, r2, DD, MM, corr; */
    /*   r1 = plist[i].corr[j].r_lower; */
    /*   r2 = plist[i].corr[j].r_upper; */
    /*   DD = plist[i].corr[j].DD; */
    /*   MM = plist[i].corr[j].MM; */
    /*   corr = plist[i].corr[j].correlation; */

    /*   fprintf(output_file, "%lf\t%lf\t%lf\t%lf\t%le\n", */
    /* 	      r1, r2, DD, MM, corr); */
    /* } */
    /* fclose(output_file); */

  }


}


/* average over lines of sight to get means and variances */
void correlation_average(POINTING *plist, int N_plist){

  if(N_plist == 1){
    fprintf(stderr, "Cannot calculate mean and variance on one pointing. \n");
    exit(EXIT_FAILURE);
  }

  int i, k;

  /* number of bins */
  int nbins = N_BINS;

  /* use this to store the mean */
  CORRELATION *corr;
  corr = calloc(nbins, sizeof(CORRELATION));

  /* initialize the r range for each bin */
  double corr_rmax_log, corr_rmin_log, corr_dr_log;
  corr_rmax_log = log10(CORR_R_MAX);
  corr_rmin_log = log10(CORR_R_MIN);
  corr_dr_log = (corr_rmax_log - corr_rmin_log) / nbins;

  for(k = 0; k < nbins; k++){
      corr[k].r_lower = pow(10.0, corr_rmin_log + k * corr_dr_log);
      corr[k].r_upper = pow(10.0, corr_rmin_log + (k + 1) * corr_dr_log);
      corr[k].r_middle = pow(10.0, corr_rmin_log + (k + 0.5) * corr_dr_log);
      corr[k].r2_lower = corr[k].r_lower * corr[k].r_lower;
      corr[k].r2_upper = corr[k].r_upper * corr[k].r_upper;
      corr[k].DD_N = 0;
      corr[k].MM_N = 0;   
      corr[k].DD = 0.0;
      corr[k].MM = 0.0;
      corr[k].correlation = 0.0;
      corr[k].sigma = 0.0;
      corr[k].sigma2 = 0.0;
      corr[k].sigma2_dd = 0.0;
      corr[k].sigma2_mm = 0.0;
  }

  POINTING *p;
  
  for(k = 0; k < nbins; k++){

    double mean_dd_n = 0.0, mean_mm_n = 0.0; /* temporary holder for mean of raw pair counts */

    /* calculate the mean */
    for(i = 0; i < N_plist; i++){
      p = &plist[i];
      corr[k].DD += p->corr[k].DD;
      corr[k].MM += p->corr[k].MM;
      mean_dd_n += p->corr[k].DD_N;
      mean_mm_n += p->corr[k].MM_N;
      corr[k].correlation += p->corr[k].correlation;
    }

    corr[k].DD /= N_plist;
    corr[k].MM /= N_plist;
    mean_dd_n /= N_plist;
    mean_mm_n /= N_plist;
    corr[k].correlation /= N_plist;

    /* calculate the variances */
    for(i = 0; i < N_plist; i++){
      p = &plist[i];
      corr[k].sigma2 += ((p->corr[k].correlation - corr[k].correlation) 
				     * (p->corr[k].correlation - corr[k].correlation));
      corr[k].sigma2_dd += ((p->corr[k].DD - corr[k].DD) 
			    * (p->corr[k].DD - corr[k].DD));
      corr[k].sigma2_mm += ((p->corr[k].MM - corr[k].MM) 
			    * (p->corr[k].MM - corr[k].MM));

      corr[k].sigma2_dd_n += ((p->corr[k].DD_N - mean_dd_n) 
			      * (p->corr[k].DD_N - mean_dd_n));
      corr[k].sigma2_mm_n += ((p->corr[k].MM_N - mean_mm_n) 
			      * (p->corr[k].MM_N - mean_mm_n));

    }

    corr[k].sigma2 /= (N_plist - 1);
    corr[k].sigma2_dd /= (N_plist - 1);
    corr[k].sigma2_mm /= (N_plist - 1);
    corr[k].sigma2_dd_n /= (N_plist - 1);
    corr[k].sigma2_mm_n /= (N_plist - 1);
    corr[k].sigma = sqrt(corr[k].sigma2);

    corr[k].DD_N = (int)mean_dd_n;
    corr[k].MM_N = (int)mean_mm_n;

  }

  /* output mean */
  char data_dir[256];
  snprintf(data_dir, 256, "./data/");

  char output_filename[256];
  FILE *output_file;
  snprintf(output_filename, 256, "%scorrelation.dat", data_dir);
  output_file = fopen(output_filename, "w");

  for(k = 0; k < nbins; k++){

    double err = corr[k].sigma / sqrt(N_plist);

    fprintf(output_file, "%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%ld\t%ld\t%le\t%le\t%le\t%le\t%le\t%le\t%le\n",
	    corr[k].r_lower, corr[k].r_upper, corr[k].r_middle,
	    corr[k].DD, corr[k].MM, corr[k].correlation,
	    corr[k].DD_N, corr[k].MM_N,
	    corr[k].sigma2_dd, corr[k].sigma2_mm, 
	    corr[k].sigma2_dd_n, corr[k].sigma2_mm_n, 
	    corr[k].sigma2, corr[k].sigma, 
	    err);

  }

  fclose(output_file);

  fprintf(stderr, "Mean and variance results output to %s.\n", output_filename);

}
