#include "mcmc.h"

/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* -----------------------  I / O data functions  ------------------------ */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */


/* ----------------------------------------------------------------------- */

/* Load unique ID of each pointing */
void load_pointingID(int *N_plist, POINTING **plist){

    char plist_filename[256];
    snprintf(plist_filename, 256, "%spointing_ID.dat", RAW_DIR);

    FILE *plist_file;
    int N;
    POINTING *p;

    if((plist_file=fopen(plist_filename,"r"))==NULL){
        fprintf(stderr, "Error: Cannot open file %s \n", plist_filename);
        exit(EXIT_FAILURE);
    }

    /* First get length of list */
    fscanf(plist_file, "%d", &N);

    /* Claim array for list of pointings */
    p = calloc(N, sizeof(POINTING));

    /* Get pointing IDs */
    int i;
    for(i=0; i<N; i++){
        fscanf(plist_file, "%s", p[i].ID);
    }
    fclose(plist_file);

    /* Assign values to main function arguments */
    *N_plist = N;
    *plist = p;

}

/* ----------------------------------------------------------------------- */

/* Load number of bins. Bin edge values are not needed in chain. */
int load_Nbins(void){

    int N;
    char bin_filename[256];
    FILE *bin_file;
    snprintf(bin_filename, 256, "%srbins.ascii.dat", BINS_DIR);
    if((bin_file=fopen(bin_filename,"r"))==NULL){
        fprintf(stderr, "Error: Cannot open file %s \n", bin_filename);
        exit(EXIT_FAILURE);
    }
    fscanf(bin_file, "%d", &N);
    fclose(bin_file);

    return N;
}

/* ----------------------------------------------------------------------- */

/* Load position and density weight data for model stars */
void load_ZRW(POINTING *plist, int lower_ind, int upper_ind, int rank){

    char zrw_filename[256];
    FILE *zrw_file;
    int i, j, N;
    double * Z;
    double * R;
    double * W;

    /* Read star data for each poiting */
    for(i = lower_ind; i < upper_ind; i++){

        snprintf(zrw_filename, 256, "%smodel_ZRW_%s.dat", ZRW_DIR, plist[i].ID);
        if((zrw_file=fopen(zrw_filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s \n", zrw_filename);
            exit(EXIT_FAILURE);
        }
        fscanf(zrw_file, "%d", &N); /* read in number of stars */

        /* Claim arrays */
        Z = calloc(N, sizeof(double));
        R = calloc(N, sizeof(double));
        W = calloc(N, sizeof(double));

        /* Read file for zrw data */
        for(j=0; j<N; j++){
            fscanf(zrw_file, "%lf", &Z[j]);
            fscanf(zrw_file, "%lf", &R[j]);
            fscanf(zrw_file, "%lf", &W[j]);
        }

        fclose(zrw_file);

        /* Assign value to plist element */
        plist[i].N_stars = N;
        plist[i].Z = Z;
        plist[i].R = R;
        plist[i].weight = W;
    }

    if(rank==0) fprintf(stderr, "Model data loaded from %s\n", ZRW_DIR);
}

/* ----------------------------------------------------------------------- */

/* Load data for each bin from a variety of files */
void load_rbins(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank){

    char filename[256];
    FILE *file;
    int i, j;
    RBIN *b;

    /* Loop over each pointing */
    for( i = lower_ind; i<upper_ind; i++ ){

        /* Claim space for bin data */
        b = calloc(N_bins, sizeof(RBIN));

        /* First load DD counts */
        /* Also assign Bin ID */
        snprintf(filename, 256, "%sdd_%s.dat", DD_DIR, plist[i].ID);
        if((file=fopen(filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s\n", filename);
            exit(EXIT_FAILURE);
        }
        for( j=0; j<N_bins; j++ ){
            fscanf(file, "%lf", &b[j].DD);
            snprintf(b[j].binID, 256, "%d", j);
        }
        fclose(file);

        /* Next load RR counts */
        snprintf(filename, 256, "%suniform_rr_%s.dat", RR_DIR, plist[i].ID);
        if((file=fopen(filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s\n", filename);
            exit(EXIT_FAILURE);
        }
        for( j=0; j<N_bins; j++ ){
            fscanf(file, "%lf", &b[j].RR);
            snprintf(b[j].binID, 256, "%d", j);
        }
        fclose(file);

        /* Assign values to plist elements */
        plist[i].rbin = b;
    }
    if(rank==0){
        fprintf(stderr, "DD counts loaded from %s\n", DD_DIR);
        fprintf(stderr, "RR counts loaded from %s\n", RR_DIR);
    }
}

/* ----------------------------------------------------------------------- */

/* Load pairs for each bin in each l.o.s. */
void load_pairs(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank){

    char pair_filename[256];
    FILE *pair_file;
    int i, j;
    unsigned int k, N;
    int *pair1;
    int *pair2;

    /* Loop over each pointing */
    for(i=lower_ind; i<upper_ind; i++){

        for(j=0; j<N_bins; j++){
            snprintf(pair_filename, 256, "%scounts_%s.bin_%s.dat", PAIRS_DIR,
                plist[i].ID, plist[i].rbin[j].binID);
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

            /* Assign values to plist elements */
            plist[i].rbin[j].N_pairs = N;
            plist[i].rbin[j].pair1 = pair1;
            plist[i].rbin[j].pair2 = pair2;
        }

    }
    if(rank == 0)fprintf(stderr, "Pairs loaded from %s\n", PAIRS_DIR);
}

/* ----------------------------------------------------------------------- */

/* load the inverted covariance matrix from mock pair counts */
void load_inv_covariance(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank){

    char invcov_filename[256];
    FILE *invcov_file;
    int i, j, k;
    INVCOV *row;
    double *col;

    /* Loop over each pointing */
    for(i=lower_ind; i<upper_ind; i++){

        /* First assign covariance matrix terms */

        /* Claim space for bin data */
        row = calloc(N_bins, sizeof(INVCOV));

        /* read in file */
        snprintf(invcov_filename, 256, "%sinv_covariance_%s.dat", ERR_DIR, plist[i].ID);
        if((invcov_file=fopen(invcov_filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s\n", invcov_filename);
            exit(EXIT_FAILURE);
        }

        /* loop over rows covariance matrix, reading in data */
        for(j=0; j<N_bins; j++){

            /* claim array for columns */
            col = calloc(N_bins, sizeof(double));

            for(k=0; k<N_bins; k++){
                fscanf(invcov_file, "%le", &col[k]);
            }

            /* assign each column element to its row */
            row[j].invcov_col = col;
        }

        fclose(invcov_file);

        /* Assign values to plist elements */
        plist[i].invcov_row = row;
    }


    if(rank == 0)fprintf(stderr, "Covariance matrix loaded from %s\n", ERR_DIR);

}

// /* load the covariance matrix from mock pair counts */
// void load_covariance(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank){

//     char cov_filename[256];
//     FILE *cov_file;
//     int i, j, k;
//     COV *row;
//     double *col;

//     /* Loop over each pointing */
//     for(i=lower_ind; i<upper_ind; i++){

//         /* First assign covariance matrix terms */

//         /* Claim space for bin data */
//         row = calloc(N_bins, sizeof(COV));

//         /* read in file */
//         snprintf(cov_filename, 256, "%scovariance_%s.dat", ERR_DIR, plist[i].ID);
//         if((cov_file=fopen(cov_filename,"r"))==NULL){
//             fprintf(stderr, "Error: Cannot open file %s\n", cov_filename);
//             exit(EXIT_FAILURE);
//         }

//         /* loop over rows covariance matrix, reading in data */
//         for(j=0; j<N_bins; j++){

//             /* claim array for columns */
//             col = calloc(N_bins, sizeof(double));

//             for(k=0; k<N_bins; k++){
//                 fscanf(cov_file, "%le", &col[k]);
//             }

//             /* assign each column element to its row */
//             row[j].cov_col = col;
//         }

//         fclose(cov_file);

//         /* Assign values to plist elements */
//         plist[i].cov_row = row;
//     }


//     if(rank == 0)fprintf(stderr, "Covariance matrix loaded from %s\n", ERR_DIR);

// }

//  load the correlation matrix from mock pair counts
// void load_correlation(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank){

//     char cor_filename[256];
//     FILE *cor_file;
//     int i, j, k;
//     COR *row;
//     double *col;

//     /* Loop over each pointing */
//     for(i=lower_ind; i<upper_ind; i++){

//         /* First assign correlation matrix terms */

//         /* Claim space for bin data */
//         row = calloc(N_bins, sizeof(COR));

//         /* read in file */
//         snprintf(cor_filename, 256, "%scorrelation_%s.dat", ERR_DIR, plist[i].ID);
//         if((cor_file=fopen(cor_filename,"r"))==NULL){
//             fprintf(stderr, "Error: Cannot open file %s\n", cor_filename);
//             exit(EXIT_FAILURE);
//         }

//         /* loop over rows correlation matrix, reading in data */
//         for(j=0; j<N_bins; j++){

//             /* claim array for columns */
//             col = calloc(N_bins, sizeof(double));

//             for(k=0; k<N_bins; k++){
//                 fscanf(cor_file, "%le", &col[k]);
//             }

//             /* assign each column element to its row */
//             row[j].cor_col = col;
//         }

//         fclose(cor_file);

//         /* Assign values to plist elements */
//         plist[i].cor_row = row;
//     }
//     if(rank == 0)fprintf(stderr, "Correlation matrix loaded from %s\n", ERR_DIR);

// }


/* ----------------------------------------------------------------------- */

/* Load starting data for MCMC loop */
void load_step_data(STEP_DATA *step_data, int flag, int rank){

    if(flag==0){
        if(rank==0) fprintf(stderr, "Testing correct parameters.\n");
        step_data->thin_r0  = 2.34;
        step_data->thin_z0  = 0.233;
        step_data->thick_r0 = 2.51;
        step_data->thick_z0 = 0.674;
        step_data->ratio_thick_thin = 0.1;
    }
    else if(flag==1){
        if(rank==0) fprintf(stderr, "Starting parameters greater than true.\n");
        step_data->thin_r0  = 3.0;
        step_data->thin_z0  = 0.3;
        step_data->thick_r0 = 4.0;
        step_data->thick_z0 = 1.2;
        step_data->ratio_thick_thin = 0.12;
    }
    else if(flag==-1){
        if(rank==0) fprintf(stderr, "Starting parameters less than true.\n");
        step_data->thin_r0  = 1.8;
        step_data->thin_z0  = 0.1;
        step_data->thick_r0 = 2.0;
        step_data->thick_z0 = 0.3;
        step_data->ratio_thick_thin = 0.5;
    }
    else{
        fprintf(stderr, "Parameter flag unrecognized. Pass -1, 0, or 1.\n");
        exit(EXIT_FAILURE);
    }
}

/* ----------------------------------------------------------------------- */


/* Output mcmc data to a file */
void output_mcmc(int index, STEP_DATA p, FILE *output_file){

    /* Output column headers as first line */
    if(index==0){
        fprintf( output_file, "step\tchi2\tchi2_red\tr0_thin\tz0_thin\tr0_thick\tz0_thick\tratio\n");
    }

    fprintf( output_file, "%d\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\n",
        index, p.chi2, p.chi2_reduced, p.thin_r0, p.thin_z0,
        p.thick_r0, p.thick_z0, p.ratio_thick_thin );
}

/* ----------------------------------------------------------------------- */
