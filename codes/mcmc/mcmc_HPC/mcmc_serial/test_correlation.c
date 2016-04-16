#include "config.h"

int main(int argc, char* argv[]){

  if (argc != 1){
    fprintf( stderr, "Usage: %s\n", argv[0]);
    exit(EXIT_FAILURE);
  }

  int i;

  int N_plist;
  POINTING *plist;
  load_pointing_list(&N_plist, &plist);

  /* Read data */
  load_data(N_plist, plist);

  /* Read model data for each pointing, 
     here each file starts with uniformly distributed random */
  load_model(N_plist, plist);
  
  /* initialize model parameters */
  PARAMETERS params;
  load_parameters(&params);

  /* set weights to model */
  set_weights(params, plist, N_plist);

  fprintf(stderr, "Start correlation calculation..\n");

  double CORR_R_MIN = 0.005;
  double CORR_R_MAX = 2.0;
  int N_BINS = 12;

  double corr_rmax_log, corr_rmin_log, corr_dr_log;
  corr_rmax_log = log10(CORR_R_MAX);
  corr_rmin_log = log10(CORR_R_MIN);
  corr_dr_log = (corr_rmax_log - corr_rmin_log) / N_BINS;

  for(i = 0; i < N_plist; i++){

    POINTING *p;
    int k;

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

    /* counting pairs for data and model, then calculate correlations */
    pairs_los_data(p);

    pairs_los_model(p);

    correlation_los(p);

  }


  int dof = degrees_of_freedom(plist, N_plist, params);

  double chi2 = chi_square(plist, N_plist);

  fprintf(stderr, "dof = %d, chi2 = %le \n", dof, chi2);


  /* output correlation results */

  for(i = 0; i < N_plist; i++){

    char output_filename[256];
    FILE *output_file;
    int k;
    snprintf(output_filename, 256, "%scorrelation_%s.dat", DATA_DIR, plist[i].ID);
    output_file = fopen(output_filename, "w");
    for(k = 0; k < plist[i].N_corr; k++){
      double r1, r2, rm, DD, MM, corr;
      r1 = plist[i].corr[k].r_lower;
      r2 = plist[i].corr[k].r_upper;
      rm = plist[i].corr[k].r_middle;
      DD = plist[i].corr[k].DD;
      MM = plist[i].corr[k].MM;
      corr = plist[i].corr[k].correlation;
      long DD_N, MM_N; 
      double sigma2_dd, sigma2_mm, sigma2, chi2;
      DD_N = plist[i].corr[k].DD_N;
      MM_N = plist[i].corr[k].MM_N;
      sigma2_dd = plist[i].corr[k].sigma2_dd;
      sigma2_mm = plist[i].corr[k].sigma2_mm;
      sigma2 = plist[i].corr[k].sigma2;
      chi2 = plist[i].corr[k].chi2;

      fprintf(output_file, "%lf\t%lf\t%lf\t%lf\t%lf\t%le\t%ld\t%ld\t%le\t%le\t%le\t%le\n",
    	      r1, r2, rm, DD, MM, corr, DD_N, MM_N, sigma2_dd, sigma2_mm, sigma2, chi2);
    }
    fclose(output_file);

  }

  fprintf(stderr, "Correlation results output to %s.\n", DATA_DIR);

  /* calculate the mean and variance */
  correlation_average(plist, N_plist);


  /* clean up */
  for(i = 0; i < N_plist; i++){
    free(plist[i].data);
    free(plist[i].model);
    free(plist[i].corr);
  }
  free(plist);

  return EXIT_SUCCESS;

}





