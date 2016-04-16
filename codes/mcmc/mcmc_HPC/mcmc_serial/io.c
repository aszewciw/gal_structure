/* Functions to read specific files */
#include "config.h"


void load_parameters(PARAMETERS *params){

  params->N_parameters = 5; 	/* Total number of free paramters. */

  params->thindisk_type = 1;	/* turn on thin disk */
  params->thindisk_r0 = 3.0;
  params->thindisk_z0 = 0.3;
  params->thindisk_n0 = 1.0;

  params->thickdisk_type = 1;	/* turn on thick disk */
  params->thickdisk_r0 = 4.0;
  params->thickdisk_z0 = 1.2;
  params->n0_ratio_thick_thin = 0.1;
  params->thickdisk_n0 = params->n0_ratio_thick_thin * params->thindisk_n0;

  params->halo_type = 0; 	/* turn off halo */

  fprintf(stderr, "Default initial parameters set..\n");

}


/* load the list of pointing info */
void load_pointing_list(int *N_plist, POINTING **plist){

  char plist_filename[256];
  snprintf(plist_filename, 256, "%stodo_list.ascii.dat", DATA_DIR);

  FILE *plist_file;
  int N;
  POINTING *p;

  if((plist_file=fopen(plist_filename,"r"))==NULL){
    fprintf(stderr,"Error: Cannot open file %s \n", plist_filename);
    exit(EXIT_FAILURE);
  }

  fprintf(stderr, "Read pointing list from %s \n", plist_filename);

  fscanf(plist_file, "%d", &N); /* first read in the length of the list */

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

  fprintf(stderr, "%d pointings to do.\n", N);
}


void load_data(int N_plist, POINTING *plist){

  char data_filename[256];
  FILE *data_file;
  int i, j, N;
  STAR *p;

  /* Read star data for each pointing */
  for(i = 0; i < N_plist; i++){
    snprintf(data_filename, 256, "%sstar_%s.ascii.dat", DATA_DIR, plist[i].ID);

    if((data_file=fopen(data_filename,"r"))==NULL){
      fprintf(stderr,"Error: Cannot open file %s \n", data_filename);
      exit(EXIT_FAILURE);
    }

    fscanf(data_file, "%d", &N); /* first read in the length of the list */

    /* Claim an array */
    p = calloc(N, sizeof(STAR));

    for(j = 0; j < N; j++){
      fscanf(data_file, "%lf", &p[j].ra_rad);
      fscanf(data_file, "%lf", &p[j].dec_rad);
      fscanf(data_file, "%lf", &p[j].distance);
      fscanf(data_file, "%lf", &p[j].galactic_l_rad);
      fscanf(data_file, "%lf", &p[j].galactic_b_rad);
      fscanf(data_file, "%lf", &p[j].galactic_Z);
      fscanf(data_file, "%lf", &p[j].galactic_R);
      fscanf(data_file, "%lf", &p[j].x);
      fscanf(data_file, "%lf", &p[j].y);
      fscanf(data_file, "%lf", &p[j].z);
      fscanf(data_file, "%lf", &p[j].weight);
    }

    fclose(data_file);

    /* Assign the value to the plist element */
    plist[i].N_data = N;
    plist[i].data = p;

  }

  fprintf(stderr, "Star data loaded from %s\n", DATA_DIR);

}

void load_model(int N_plist, POINTING *plist){

  char data_filename[256];
  FILE *data_file;
  int i, j, N;
  STAR *p;

  /* Read star data for each pointing */
  for(i = 0; i < N_plist; i++){
    snprintf(data_filename, 256, "%suniform_%s.ascii.dat", DATA_DIR, plist[i].ID);

    if((data_file=fopen(data_filename,"r"))==NULL){
      fprintf(stderr,"Error: Cannot open file %s \n", data_filename);
      exit(EXIT_FAILURE);
    }

    fscanf(data_file, "%d", &N); /* first read in the length of the list */

    /* Claim an array */
    p = calloc(N, sizeof(STAR));

    for(j = 0; j < N; j++){
      fscanf(data_file, "%lf", &p[j].ra_rad);
      fscanf(data_file, "%lf", &p[j].dec_rad);
      fscanf(data_file, "%lf", &p[j].distance);
      fscanf(data_file, "%lf", &p[j].galactic_l_rad);
      fscanf(data_file, "%lf", &p[j].galactic_b_rad);
      fscanf(data_file, "%lf", &p[j].galactic_Z);
      fscanf(data_file, "%lf", &p[j].galactic_R);
      fscanf(data_file, "%lf", &p[j].x);
      fscanf(data_file, "%lf", &p[j].y);
      fscanf(data_file, "%lf", &p[j].z);
      fscanf(data_file, "%lf", &p[j].weight);
    }

    fclose(data_file);

    /* Assign the value to the plist element */
    plist[i].N_model = N;
    plist[i].model = p;

  }

  fprintf(stderr, "Model data loaded from %s\n", DATA_DIR);

}


void load_errors(int N_plist, POINTING *plist){

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



