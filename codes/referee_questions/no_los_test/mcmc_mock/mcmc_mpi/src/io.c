#include "mcmc.h"

/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* -----------------------  I / O data functions  ------------------------ */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */


/* ----------------------------------------------------------------------- */

/* Load position and density weight data for model stars */
void load_ZR(MODEL *m, int rank){
    fprintf(stderr, "here\n");
    char zr_filename[256];
    FILE *zr_file;
    int j, N;
    double * Z;
    double * R;
    double * W;

    snprintf(zr_filename, 256, "%srandom_ZR.dat", ZR_DIR);
    if((zr_file=fopen(zr_filename,"r"))==NULL){
        fprintf(stderr, "Error: Cannot open file %s \n", zr_filename);
        exit(EXIT_FAILURE);
    }

    fscanf(zr_file, "%d", &N); /* read in number of stars */

    Z = calloc(N, sizeof(double));
    R = calloc(N, sizeof(double));
    W = calloc(N, sizeof(double));

    /* Read file for zr data */
    for(j=0; j<N; j++){
        fscanf(zr_file, "%lf", &Z[j]);
        fscanf(zr_file, "%lf", &R[j]);
        W[j] = 1.0;
    }

    fclose(zr_file);

    fprintf(stderr, "Made it here\n");

    /* Assign value to m element */
    m->N_stars = N;
    m->Z = Z;
    m->R = R;
    m->weight = W;

    fprintf(stderr, "Made iere\n");


    if(rank==0) fprintf(stderr, "Model data loaded from %s\n", ZR_DIR);
}

/* ----------------------------------------------------------------------- */

/* Load data for each bin from a variety of files */
void load_rbins(MODEL *m, int N_bins, int rank){

    char filename[256];
    FILE *file;
    int i, j;
    RBIN *b;

    /* Claim space for bin data */
    b = calloc(N_bins, sizeof(RBIN));

    /* First load DD counts */
    /* Also assign Bin ID */
    snprintf(filename, 256, "%sdd.dat", DD_DIR);
    if((file=fopen(filename,"r"))==NULL){
        fprintf(stderr, "Error: Cannot open file %s\n", filename);
        exit(EXIT_FAILURE);
    }
    for( j=0; j<N_bins; j++ ){
        fscanf(file, "%lf", &b[j].DD);
        snprintf(b[j].binID, 256, "%d", j);
    }
    fclose(file);

    /* Next load DD errors */
    snprintf(filename, 256, "%smock_frac_error.dat", ERR_DIR);
    if((file=fopen(filename,"r"))==NULL){
        fprintf(stderr, "Error: Cannot open file %s\n", filename);
        exit(EXIT_FAILURE);
    }
    for(j=0; j<N_bins; j++){
        fscanf(file, "%lf", &b[j].DD_err_jk);
    }
    fclose(file);

    /* Next load MM errors */
    snprintf(filename, 256, "%suniform_frac_error.dat", ERR_DIR);
    if((file=fopen(filename,"r"))==NULL){
        fprintf(stderr, "Error: Cannot open file %s\n", filename);
        exit(EXIT_FAILURE);
    }
    for(j=0; j<N_bins; j++){
        fscanf(file, "%lf", &b[j].MM_err_jk);
    }
    fclose(file);

    /* Assign values to m elements */
    m[i].rbin = b;

    if(rank==0){
        fprintf(stderr, "DD counts loaded from %s\n", DD_DIR);
        fprintf(stderr, "Errors loaded from %s\n", ERR_DIR);
    }
}

/* ----------------------------------------------------------------------- */

/* have each proc load a list of pairs with the corresponding bin ID */
void load_pairs(MODEL *m, int rank){

    char pair_filename[256];
    FILE *pair_file;
    int j;
    unsigned int k, N;
    int *pair1;
    int *pair2;

    /* Loop over each pointing */
    snprintf(pair_filename, 256, "%scounts_bin_%d.dat", PAIRS_DIR, rank);
    if((pair_file=fopen(pair_filename,"r"))==NULL){
        fprintf(stderr, "Error: Cannot open file %s\n", pair_filename);
        exit(EXIT_FAILURE);
    }

    /* First get number of pairs */
    fscanf(pair_file, "%u", &N);

    /* Claim arrays */
    pair1 = calloc(N, sizeof(int));
    pair2 = calloc(N, sizeof(int));

    for(k=0; k<N; k++){
        fscanf(pair_file, "%d", &pair1[k]);
        fscanf(pair_file, "%d", &pair2[k]);
    }

    fclose(pair_file);

    /* Assign values to m elements */
    m->rbin[rank].N_pairs = N;
    m->rbin[rank].pair1   = pair1;
    m->rbin[rank].pair2   = pair2;

    if(rank == 0)fprintf(stderr, "Pairs loaded from %s\n", PAIRS_DIR);
}

/* ----------------------------------------------------------------------- */

/* Load starting data for MCMC loop */
void load_step_data(STEP_DATA *step_data){

    // step_data->thin_r0 = 3.0;
    // step_data->thin_z0 = 0.3;
    // step_data->thick_r0 = 4.0;
    // step_data->thick_z0 = 1.2;
    // step_data->ratio_thick_thin = 0.1;
    step_data->thin_r0 = 2.34;
    step_data->thin_z0 = 0.233;
    step_data->thick_r0 = 2.51;
    step_data->thick_z0 = 0.674;
    step_data->ratio_thick_thin = 0.1;
}

/* ----------------------------------------------------------------------- */


/* Output mcmc data to a file */
void output_mcmc(int index, STEP_DATA p, FILE *output_file){

    fprintf( output_file, "%d\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\n",
        index, p.chi2, p.chi2_reduced, p.thin_r0, p.thin_z0,
        p.thick_r0, p.thick_z0, p.ratio_thick_thin );
}

/* ----------------------------------------------------------------------- */
