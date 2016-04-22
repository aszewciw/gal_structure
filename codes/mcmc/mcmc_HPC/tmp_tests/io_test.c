#include "io_test.h"

/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* -----------------------  Input data functions  ------------------------ */
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

    fprintf(stderr, "Read pointing list from %s \n", plist_filename);

    fscanf(plist_file, "%d", &N); //length of list

    // Claim array for list of pointings
    p = calloc(N, sizeof(POINTING));

    // Get pointing IDs
    int i;
    for(i=0; i<N; i++){
        fscanf(plist_file, "%s", p[i].ID);
    }
    fclose(plist_file);

    // Aassign values to main function arguments
    *N_plist = N;
    *plist = p;

    fprintf(stderr, "%d pointings to do.\n", N);

}

/* ----------------------------------------------------------------------- */

/* Load position and density weight data for model stars */
void load_ZRW(int N_plist, POINTING *plist){

    char zrw_filename[256];
    FILE *zrw_file;
    int i, j, N;
    double * Z;
    double * R;
    double * W;

    /* Read star data for each poiting */
    for(i=0; i<N_plist; i++){
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

    fprintf(stderr, "Model data loaded from %s\n", ZRW_DIR);
}

/* ----------------------------------------------------------------------- */

/* Load data for each bin from a variety of files */
void load_rbins(int N_plist, int N_bins, POINTING *plist){

    char filename[256];
    FILE *file;
    int i, j;
    RBIN *b;

    /* Loop over each pointing */
    for(i=0; i<N_plist; i++){

        /* Claim space for bin data */
        b = calloc(N_bins, sizeof(RBIN));

        /* First load DD counts */
        /* Also assign Bin ID */
        snprintf(filename, 256, "%sdd_%s.dat", DD_DIR, plist[i].ID);
        if((file=fopen(filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s\n", filename);
            exit(EXIT_FAILURE);
        }
        for(j=0; j<N_bins; j++){
            fscanf(file, "%lf", &b[j].DD);
            snprintf(b[j].binID, 256, "%d", j+1);
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
    fprintf(stderr, "DD counts loaded from %s\n", DD_DIR);
    fprintf(stderr, "Errors loaded from %s\n", ERR_DIR);
}

/* ----------------------------------------------------------------------- */

/* Load pairs for each bin in each l.o.s. */
void load_pairs(int N_plist, int N_bins, POINTING *plist){

    char pair_filename[256];
    FILE *pair_file;
    int i, j;
    unsigned int k, N;
    int *pair1;
    int *pair2;

    /* Loop over each pointing */
    for(i=0; i<N_plist; i++){

        for(j=0; j<N_bins; j++){
            snprintf(pair_filename, 256, "%spairs_%s.bin_%s.dat", PAIRS_DIR, plist[i].ID, plist[i].rbin[j].binID);
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
                fscanf(pair_file, "%u", &pair1[k]);
                fscanf(pair_file, "%u", &pair2[k]);
            }

            fclose(pair_file);

            /* Assign values to plist elements */
            plist[i].rbin[j].N_pairs = N;
            plist[i].rbin[j].pair1 = pair1;
            plist[i].rbin[j].pair2 = pair2;
        }

    }
    fprintf(stderr, "Pairs loaded from %s\n", PAIRS_DIR);


}

/* ----------------------------------------------------------------------- */

/* Load starting data for MCMC loop */
void load_step_data(STEP_DATA *step_data){

    step_data->N_params = 5;
    // step_data->thin_r0 = 3.0;
    // step_data->thin_z0 = 0.3;
    // step_data->thick_r0 = 4.0;
    // step_data->thin_z0 = 1.2;
    // step_data->ratio_thick_thin = 0.1;
    step_data->thin_r0 = 2.475508;
    step_data->thin_z0 = 0.241209;
    step_data->thick_r0 = 2.417346;
    step_data->thin_z0 = 0.694395;
    step_data->ratio_thick_thin = 0.106672;

    fprintf(stderr, "Default initial parameters set...\n");

}

/* ----------------------------------------------------------------------- */



/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* ------------------  Functions calculating errors  --------------------- */
/* ----------------------- *Also used in MCMC* --------------------------- */
/* ----------------------------------------------------------------------- */

/* ----------------------------------------------------------------------- */

/* Multiply this by DD/MM**2 to get sigma2 */
void calculate_frac_error(int N_plist, int N_bins, POINTING *p){

    int i, j;

    for(i = 0; i < N_plist; i++){

        for(j = 0; j < N_bins; j++){

            p[i].rbin[j].err2_frac = (
                p[i].rbin[j].DD_err_jk * p[i].rbin[j].DD_err_jk
                + p[i].rbin[j].MM_err_jk * p[i].rbin[j].MM_err_jk );
        }
    }
}

/* ----------------------------------------------------------------------- */

void calculate_chi2( POINTING *p, STEP_DATA *step, int N_plist, int N_bins ){

    int i, j;
    step->chi2 = 0.0;

    for(i = 0; i < N_plist; i++){

        for(j = 0; j < N_bins; j++){

            p[i].rbin[j].sigma2 = ( p[i].rbin[j].corr * p[i].rbin[j].corr *
                p[i].rbin[j].err2_frac );

            if( p[i].rbin[j].sigma2 == 0.0 ) continue;

            step->chi2 += ( ( p[i].rbin[j].corr - 1.0 ) * ( p[i].rbin[j].corr - 1.0 )
                / p[i].rbin[j].sigma2 );

        }
    }
}



/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* -------------------  Functions called by MCMC  ------------------------ */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */

/* ----------------------------------------------------------------------- */
double sech2(double x){
    return 1.0 / (cosh(x) * cosh(x));
}


/* Set weights for all model points based on disk parameters */
void set_weights(STEP_DATA params, POINTING *p, int N_plist){

    int i, j;

    for(i = 0; i < N_plist; i++){

        for(j = 0; j < p[i].N_stars; j++){

            p[i].weight[j] = (
                ( sech2( p[i].Z[j] / 2.0 / params.thin_z0 )
                    * exp( -p[i].R[j] / params.thin_r0 ) )
                + params.ratio_thick_thin *
                ( sech2( p[i].Z[j] / 2.0 / params.thick_z0 )
                    * exp( -p[i].Z[j] / params.thick_r0 ) ) );
        }
    }
}

/* ----------------------------------------------------------------------- */

/* Determine normalization of MM counts */
double normalize_MM(double *weight, int N_stars){

    int i, j;
    double norm = 0.0;

    for(i = 0; i < N_stars; i++){

        for(j = 0; j < N_stars; j++){

            if(i == j) continue;

            norm += weight[i] * weight[j];
        }
    }
    norm /= 2.0;
    return norm;
}

/* ----------------------------------------------------------------------- */

/* Calculate normalized model pair counts MM for 1 bin */
double calculate_MM( unsigned int N_pairs, int *pair1, int *pair2,
    double MM_norm, double *weight ){

    unsigned int i;
    double MM = 0.0;

    for(i = 0; i < N_pairs; i++){

        MM += weight[pair1[i]] * weight[pair2[i]];

    }

    MM /= MM_norm;

    return MM;
}

/* ----------------------------------------------------------------------- */

/* Calculate correlation (DD/MM) for each bin in each l.o.s. */
void calculate_correlation(POINTING *p, int N_plist, int N_bins){

    int i, j;
    double MM_norm;

    /* Loop over l.o.s. */
    for(i = 0; i < N_plist; i++){

        MM_norm = normalize_MM(p[i].weight, p[i].N_stars);

        for(j = 0; j < N_bins; j++){

            p[i].rbin[j].MM = calculate_MM( p[i].rbin[j].N_pairs,
                p[i].rbin[j].pair1, p[i].rbin[j].pair2, MM_norm,
                p[i].weight );

            if( p[i].rbin[j].DD == 0.0 || p[i].rbin[j].MM == 0.0 ){
                p[i].rbin[j].corr = 0.0;
                continue;
            }
            p[i].rbin[j].corr = p[i].rbin[j].DD / p[i].rbin[j].MM;

        }
    }
}

/* ----------------------------------------------------------------------- */

/* Calculate degrees of freedom */
int degrees_of_freedom(POINTING *p, int N_plist, int N_bins ){
    int dof = 0;
    int i, j;

    for(i = 0; i < N_plist; i++){

        for(j = 0; j < N_bins; j++){

            if( p[i].rbin[j].sigma2 == 0.0 ) continue;

            dof++;
        }
    }

    return dof;
}

/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* --------------------------  MCMC functions  --------------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */


void run_mcmc(STEP_DATA initial_step, int max_steps, int N_plist, POINTING *plist, int N_bins){

    // int i,
    // int eff_counter;
    // double eff;
    STEP_DATA current;
    // STEP_DATA new;
    // double delta_chi2;
    int DOF;

    fprintf(stderr, "Start MCMC chain. Max steps = %d\n", max_steps);

    /* set first element with initial parameters */
    current = initial_step;

    /* set initial weights of model points */
    set_weights(current, plist, N_plist);
    fprintf(stderr, "Initial weights set \n");

    /* Calculate initial correlation value */
    calculate_correlation(plist, N_plist, N_bins);

    calculate_chi2(plist, &current, N_plist, N_bins);

    /* Degrees of freedom never change -- calculate once */
    DOF = degrees_of_freedom(plist, N_plist, N_bins);
    fprintf(stderr, "Degrees of freedom is: %d\n", DOF );

    fprintf(stderr, "Chi2 value for intital params is %f\n", current.chi2);

}



/* ----------------------------------------------------------------------- */


/* Test loading of data */
int main(int argc, char * argv[]){

    if (argc!=1){
        fprintf(stderr, "Usage: %s\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    /* -- Load data from various files --*/
    int i, j;
    int N_plist;
    int N_bins = 12;
    POINTING *plist;

    load_pointingID(&N_plist, &plist);
    load_ZRW(N_plist, plist);
    load_rbins(N_plist, N_bins, plist);
    load_pairs(N_plist, N_bins, plist);

    /* Calculate fractional error in DD/MM */
    /* This only needs to be done once because
       I have a trick for using it */
    calculate_frac_error(N_plist, N_bins, plist);

    /* -- Initialize parameters --*/
    STEP_DATA step_data;
    load_step_data(&step_data);
    int max_steps = 10000;
    run_mcmc(step_data, max_steps, N_plist, plist, N_bins);


    /* Free allocated values */
    for(i=0; i<N_plist; i++){
        for(j=0; j<N_bins; j++){
            free(plist[i].rbin[j].pair1);
            free(plist[i].rbin[j].pair2);
        }
        free(plist[i].rbin);
        free(plist[i].Z);
        free(plist[i].R);
        free(plist[i].weight);
    }
    free(plist);

    return EXIT_SUCCESS;

}