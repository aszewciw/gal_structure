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

        snprintf(zrw_filename, 256, "%suniform_ZRW_%s.dat", ZRW_DIR, plist[i].ID);
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

        /* Next load DD errors */
        snprintf(filename, 256, "%sstar_%s_frac_error.dat", ERR_DIR, plist[i].ID);
        if((file=fopen(filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s\n", filename);
            exit(EXIT_FAILURE);
        }
        for(j=0; j<N_bins; j++){
            fscanf(file, "%lf", &b[j].DD_err_jk);
        }
        fclose(file);

        /* Next load MM errors */
        snprintf(filename, 256, "%suniform_%s_frac_error.dat", ERR_DIR, plist[i].ID);
        if((file=fopen(filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s\n", filename);
            exit(EXIT_FAILURE);
        }
        for(j=0; j<N_bins; j++){
            fscanf(file, "%lf", &b[j].MM_err_jk);
        }
        fclose(file);

        /* Assign values to plist elements */
        plist[i].rbin = b;
    }
    if(rank==0){
        fprintf(stderr, "DD counts loaded from %s\n", DD_DIR);
        fprintf(stderr, "Errors loaded from %s\n", ERR_DIR);
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
            snprintf(pair_filename, 256, "%scounts_%s.bin_%s.dat", PAIRS_DIR, plist[i].ID, plist[i].rbin[j].binID);
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

/* Load starting data for MCMC loop */
void load_step_data(STEP_DATA *step_data, int flag, int rank){

    /* Putting in a number of different starting conditions with flags 2-11 */

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
    else if(flag==2){
        if(rank==0) fprintf(stderr, "Choosing random starting point.\n");

        srand(time(NULL));
        double rand1, rand2;
        double r0_min, r0_max, z0_min, z0_max, ratio_min, ratio_max;

        r0_min    = 1.0;
        r0_max    = 10.0;
        z0_min    = 0.1;
        z0_max    = 2.0;
        ratio_min = 0.01;
        ratio_max = 0.8;

        /* generate two random numbers for z0 */
        rand1 = (double)rand() / (double)RAND_MAX;
        rand1 = rand1 * (z0_max - z0_min) + z0_min;

        rand2 = (double)rand() / (double)RAND_MAX;
        rand2 = rand2 * (z0_max - z0_min) + z0_min;

        /* assign larger number to thick disk */
        if(rand2>=rand1){
            step_data->thin_z0 = rand1;
            step_data->thick_z0 = rand2;
        }
        else{
            step_data->thin_z0 = rand2;
            step_data->thick_z0 = rand1;
        }

        rand1 = (double)rand() / (double)RAND_MAX;
        rand1 = rand1 * (r0_max - r0_min) + r0_min;
        step_data->thin_r0 = rand1;

        rand1 = (double)rand() / (double)RAND_MAX;
        rand1 = rand1 * (z0_max - z0_min) + z0_min;
        step_data->thick_r0 = rand1;

        rand1 = (double)rand() / (double)RAND_MAX;
        rand1 = rand1 * (ratio_max - ratio_min) + ratio_min;
        step_data->ratio_thick_thin = rand1;

    }
    else{
        fprintf(stderr, "Parameter flag unrecognized. Pass -1, 0, or 1.\n");
        exit(EXIT_FAILURE);
    }
}

/* ----------------------------------------------------------------------- */


/* Output mcmc data to a file */
void output_mcmc(int index, STEP_DATA p, FILE *output_file){

    fprintf( output_file, "%d\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\n",
        index, p.chi2, p.chi2_reduced, p.thin_r0, p.thin_z0,
        p.thick_r0, p.thick_z0, p.ratio_thick_thin );
}

/* ----------------------------------------------------------------------- */
