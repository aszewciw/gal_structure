#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

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
  //load_parameters(&params);

  params.N_parameters = 5;     /* Total number of free paramters. */

  params.thindisk_type = 1;    /* turn on thin disk */
  params.thindisk_r0 = 3.0;
  params.thindisk_z0 = 0.3;
  params.thindisk_n0 = 1.0;

  params.thickdisk_type = 1;   /* turn on thick disk */
  params.thickdisk_r0 = 4.0;
  params.thickdisk_z0 = 1.2;
  params.n0_ratio_thick_thin = 0.1;
  params.thickdisk_n0 = params.n0_ratio_thick_thin * params.thindisk_n0;

  params.halo_type = 0;        /* turn off halo */


  /* set weights to model */
  set_weights(params, plist, N_plist);

  /* allocate space for correlation function calculation */
  /* This also does a first time correlation calculation of initial parameters. */
  /* DD pairs may only calculated once here but not later.  */
  correlation_initialize(plist, N_plist);

  /* load the jackknife fractional errors */
  load_errors(N_plist, plist);

  int dof = degrees_of_freedom(plist, N_plist, params);

  double chi2 = chi_square(plist, N_plist);

  fprintf(stderr, "dof = %d, chi2 = %le \n", dof, chi2);

  /* chi2 for each line of sight */
  FILE *output_file;
  char output_filename[256];
  snprintf(output_filename, 256, "%schi2_los.dat", DATA_DIR);
  output_file = fopen(output_filename, "w");
  for(i = 0; i < N_plist; i++){

    POINTING *p;
    p = &plist[i];

    int k;
    double chi2_los = 0.0;
    for(k = 0; k < p->N_corr; k++){

      chi2_los += p->corr[k].chi2;
    }

    fprintf(output_file, "%s\t%lf\n", p->ID, chi2_los);

  }

  fclose(output_file);


  for(i = 0; i < N_plist; i++){
    free(plist[i].data);
    free(plist[i].model);
    free(plist[i].corr);
  }
  free(plist);

  return EXIT_SUCCESS;

}





