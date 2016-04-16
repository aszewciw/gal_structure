/* Estimate the errors in correlation function calculation. */
#include "config.h"


void dd_error(POINTING *plist, int N_plist){
  
  int i, j, k;

  for(i = 0; i < N_plist; i++){
    POINTING *p;			/* a temporary holder */
    POINTING *pd;			/* a variable to store the delete-1 data */

    p = &plist[i];
    pd = calloc(1, sizeof(POINTING));
    memcpy(pd, p, sizeof(POINTING));

    /* allocate delete-1 memory for pd */
    pd->N_data -= 1;
    pd->data = calloc(pd->N_data, sizeof(STAR));
    /* allocate a separate space for pair counting */
    pd->corr = calloc(pd->N_corr, sizeof(CORRELATION));
    memcpy(pd->corr, p->corr, p->N_corr * sizeof(CORRELATION));

    CORRELATION **corr;
    *corr = calloc(p->N_data, sizeof(CORRELATION *));

    for(j = 0; j < p->N_data; j++){

      /* delete the j-th star */
      memcpy(pd->data, p->data, j * sizeof(STAR));
      if(j < pd->N_data){
	memcpy(pd->data + j, p->data + j + 1, (pd->N_data - j) * sizeof(STAR));
      }

      corr[j] = calloc(pd->N_corr, sizeof(CORRELATION));
      
      /* counting pairs for pd */
      pairs_los_data(pd);
      
      for(k = 0; k < pd->N_corr; k++){
	corr[j][k].DD_N = pd->corr[k].DD_N;
      }

    }
    
    /* calculate mean */
    CORRELATION *corr_mean;
    corr_mean = calloc(pd->N_corr, sizeof(CORRELATION));
    
    for(j = 0; j < p->N_data; j++){
      for(k = 0; k < pd->N_corr; k++){
	corr_mean[k].DD_N += corr[j][k].DD_N;
      }
      corr_mean[k].DD_N /= p->N_data;
    }

    

  }

}


void mm_error(POINTING *plist, int N_plist){

}
