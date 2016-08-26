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

  /* data directory */
  char data_dir[256];
  snprintf(data_dir, 256, "../data/");

  /* load the pointing list */
  char plist_filename[256];
  snprintf(plist_filename, 256, "%stodo_list.ascii.dat", data_dir);

  int N_plist;
  POINTING *plist;
  load_pointing_list(plist_filename, &N_plist, &plist);


  /* Read star data for each pointing */
  for(i = 0; i < N_plist; i++){
    char data_filename[256];
    snprintf(data_filename, 256, "%sstar_%s.ascii.dat", data_dir, plist[i].ID);
    load_data(data_filename, &plist[i].N_data, &plist[i].data);
  }

  fprintf(stderr, "Star data loaded from %s\n", data_dir);

  /* Read model data for each pointing,
     here each file starts with uniformly distributed random */
  for(i = 0; i < N_plist; i++){
    char model_filename[256];
    snprintf(model_filename, 256, "%suniform_%s.ascii.dat", data_dir, plist[i].ID);
    load_data(model_filename, &plist[i].N_model, &plist[i].model);
  }

  fprintf(stderr, "Uniform model data loaded from %s\n", data_dir);

  /* initialize model parameters */
  PARAMETERS params;
  params.N_parameters = 5; 	/* Total number of free paramters. */

  params.thindisk_type = 1;	/* turn on thin disk */
  params.thindisk_r0 = 2.475508;
  params.thindisk_z0 = 0.241209;
  params.thindisk_n0 = 1.0;

  params.thickdisk_type = 1;	/* turn on thick disk */
  params.thickdisk_r0 = 2.417346;
  params.thickdisk_z0 = 0.694395;
  params.thickdisk_n0 = 0.106672;

  params.halo_type = 0; 	/* turn off halo */

  fprintf(stderr, "Set initial parameters..\n");

  int mcmc_steps, efficiency_counter;
  double efficiency;
  MCMC *mcmc_chain;
  double chi2, delta_chi2;
  int dof;

  mcmc_steps = 500000;
  mcmc_chain = calloc(mcmc_steps, sizeof(MCMC));

  FILE *file_chain_realtime;
  file_chain_realtime = fopen("./data/mcmc.dat", "a");

  fprintf(stderr, "Allocate MCMC chain..Max steps = %d \n", mcmc_steps);

  /* set the first element as the initial parameters.
   Then calculate the chi2 for the initial parameters. */
  mcmc_chain[0].params = params;

  set_weights(mcmc_chain[0].params, plist, N_plist);

  /* allocate space for correlation function calculation */
  /* This also does a first time correlation calculation of initial parameters. */
  /* DD pairs may only calculated once here but not later.  */
  correlation_initialize(plist, N_plist);

  /* load the jackknife fractional errors */
  load_errors(plist, N_plist);

  mcmc_chain[0].dof = degrees_of_freedom(plist, N_plist, params);
  mcmc_chain[0].chi2 = chi_square(plist, N_plist);

  fprintf(stderr, "initial: chi2 = %le \n", mcmc_chain[0].chi2);

  fprintf(stderr, "Start MCMC calculation..\n");

  /* Markov chain loop */
  efficiency_counter = 1;
  for(i = 1; i < mcmc_steps; i++){

    /* update new positions in paramter space */
    params = update_parameters(mcmc_chain[i - 1].params);

    /* recalculate weights */
    set_weights(params, plist, N_plist);

    /* recalculate correlation functions */
    calculate_correlation(plist, N_plist);

    /* get chi squares */
    dof = degrees_of_freedom(plist, N_plist, params);

    chi2 = chi_square(plist, N_plist);

    delta_chi2 = chi2 - mcmc_chain[i - 1].chi2;

    fprintf(stderr, "delta_chi2 = %le \n", delta_chi2);

    if(delta_chi2 <= 0.0){
      /* if delta chisquare is smaller then record*/
      mcmc_chain[i].params = params;
      mcmc_chain[i].chi2 = chi2;
      mcmc_chain[i].dof = dof;
      efficiency_counter++;
    }
    else{
      /* if delta chisquare is bigger then use probability to decide */
      /* !!! replace with GSL random generator later !!! */
      double tmp = (double)rand() / (double)RAND_MAX; /* a random number in [0,1] */
      if (tmp < exp(- delta_chi2 / 2.0)){
	mcmc_chain[i].params = params;
	mcmc_chain[i].chi2 = chi2;
	mcmc_chain[i].dof = dof;
	efficiency_counter++;
      }
      else{
	/* record the old position. */
	mcmc_chain[i] = mcmc_chain[i - 1];
      }
    }

    efficiency = (float) efficiency_counter / i;
    /* print out progress */
    /* if(i % (mcmc_steps / 100) == 0){ */
    /*   fprintf(stderr, "MCMC... %d / %d: chi2 = %lf \n", i, mcmc_steps, chi2); */
    /* } */
    fprintf(stderr, "MCMC... %d / %d: efficiency = %lf \n z0_thin = %lf, r0_thin = %lf, z0_thick = %lf, r0_thick = %lf, n0_thick = %lf \n chi2 = %lf, dof = %d, chi2_reduced = %lf \n\n",
	    i, mcmc_steps, efficiency, params.thindisk_z0, params.thindisk_r0, params.thickdisk_z0, params.thickdisk_r0, params.thickdisk_n0, chi2, dof, chi2/dof);

    MCMC tmp_mc;
    PARAMETERS tmp_p;
    tmp_mc = mcmc_chain[i];
    tmp_p = tmp_mc.params;
    fprintf(stderr, "Made it here\n");
    fprintf(file_chain_realtime, "%d\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%d\t%lf\n",
	    i+50000, tmp_p.thindisk_r0, tmp_p.thindisk_z0, tmp_p.thickdisk_r0, tmp_p.thickdisk_z0, tmp_p.thickdisk_n0,
	    tmp_mc.chi2, (int)tmp_mc.dof, tmp_mc.chi2/dof);
    fprintf(stderr, "Printed to file.\n");
    if(i % 50 == 0){
      fflush(file_chain_realtime);
    }

  } /* end of mcmc */


  output_mcmc(mcmc_chain, mcmc_steps);

  fprintf(stderr, "End MCMC calculation..\n");

  for(i = 0; i < N_plist; i++){
    free(plist[i].data);
    free(plist[i].model);
    free(plist[i].corr);
  }
  free(plist);

  free(mcmc_chain);

  return EXIT_SUCCESS;

}





