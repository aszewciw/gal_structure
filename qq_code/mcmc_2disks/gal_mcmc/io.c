/* Functions to read specific files */

#include <stdlib.h>
#include <stdio.h>

#include "config.h"


/* load the list of pointing info */
void load_pointing_list(char *plist_filename, int *N_plist, POINTING **plist){

  FILE *plist_file;
  int N;
  POINTING *p;

  if((plist_file=fopen(plist_filename,"r"))==NULL){
    fprintf(stderr,"Error: Cannot open file %s \n", plist_filename);
    exit(EXIT_FAILURE);
  }

  fprintf(stderr, "Read pointing list from %s \n", plist_filename);

  fscanf(plist_file, "%d", &N); /* first read in the length of the list */
    
  fprintf(stderr, "%d pointings to be done.\n", N);

  /* Claim an array for a list of pointing */
  p = calloc(N, sizeof(POINTING));

  int i;
  for(i = 0; i < N; i++){
    fscanf(plist_file, "%s", p[i].ID);
    fscanf(plist_file, "%lf", &p[i].ra_deg);
    fscanf(plist_file, "%lf", &p[i].dec_deg);
    fscanf(plist_file, "%lf", &p[i].ra_rad);
    fscanf(plist_file, "%lf", &p[i].dec_rad);
    fscanf(plist_file, "%lf", &p[i].galactic_l_rad);
    fscanf(plist_file, "%lf", &p[i].galactic_b_rad);
    fscanf(plist_file, "%lf", &p[i].x);
    fscanf(plist_file, "%lf", &p[i].y);
    fscanf(plist_file, "%lf", &p[i].z);
    fscanf(plist_file, "%d", &p[i].N_data);
  }

  fclose(plist_file);
  /* Assign the value to main function arguments */
  *N_plist = N;
  *plist = p;

}


void load_data(char *data_filename, int *N_data, STAR **data){

  FILE *data_file;
  int N;
  STAR *p;

  if((data_file=fopen(data_filename,"r"))==NULL){
    fprintf(stderr,"Error: Cannot open file %s \n", data_filename);
    exit(EXIT_FAILURE);
  }

  fscanf(data_file, "%d", &N); /* first read in the length of the list */


  /* Claim an array for a list of pointing */
  p = calloc(N, sizeof(STAR));

  int i;
  for(i = 0; i < N; i++){
    fscanf(data_file, "%lf", &p[i].ra_rad);
    fscanf(data_file, "%lf", &p[i].dec_rad);
    fscanf(data_file, "%lf", &p[i].distance);
    fscanf(data_file, "%lf", &p[i].galactic_l_rad);
    fscanf(data_file, "%lf", &p[i].galactic_b_rad);
    fscanf(data_file, "%lf", &p[i].galactic_Z);
    fscanf(data_file, "%lf", &p[i].galactic_R);
    fscanf(data_file, "%lf", &p[i].x);
    fscanf(data_file, "%lf", &p[i].y);
    fscanf(data_file, "%lf", &p[i].z);
    fscanf(data_file, "%lf", &p[i].weight);
  }

  //fprintf(stderr, "Read %d stars from %s \n", N, data_filename);

  fclose(data_file);
  /* Assign the value to main function arguments */
  *N_data = N;
  *data = p;

}

CORRELATION * load_rbins(char *bins_filename, int *N_rbins){
  FILE *bins_file;
  if((bins_file=fopen(bins_filename,"r"))==NULL){
    fprintf(stderr,"Error: Cannot open file %s \n", bins_filename);
    exit(EXIT_FAILURE);
  }

  /* read the number of bins first */
  int N;
  fscanf(bins_file, "%d", &N);

  *N_rbins = N; 

  CORRELATION *corr;
  corr = calloc(N, sizeof(CORRELATION));

  int i;
  for(i = 0; i < N; i++){
    fscanf(bins_file, "%lf", &corr[i].r_lower);
    fscanf(bins_file, "%lf", &corr[i].r_upper);
    fscanf(bins_file, "%lf", &corr[i].r_middle);
    fscanf(bins_file, "%lf", &corr[i].bin_size);
  }

  fclose(bins_file);

  return corr;
}



