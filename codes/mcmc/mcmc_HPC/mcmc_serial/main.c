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

  /* allocate space for correlation bins */
  /* need to be done before load_errors */
  correlation_initialize(plist, N_plist);

  /* load the jackknife fractional errors */
  load_errors(N_plist, plist);

  
  //fprintf(stderr, "%lf\t%lf\n",plist[0].corr[0].err_jk_dd, plist[0].corr[0].err_jk_mm);


  /* initialize model parameters */
  PARAMETERS params;
  load_parameters(&params);

  /* run mcmc */
  int max_steps = 500000;
  run_mcmc(params, max_steps, N_plist, plist);


  /* clean up */
  for(i = 0; i < N_plist; i++){
    free(plist[i].data);
    free(plist[i].model);
    free(plist[i].corr);
  }
  free(plist);

  return EXIT_SUCCESS;

}





