#include "io_test.h"

#include <gsl/gsl_rng.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_integration.h>

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
    float * Z;
    float * R;
    float * W;

    /* Read star data for each poiting */
    for(i=0; i<N_plist; i++){
        snprintf(zrw_filename, 256, "%suniform_ZRW_%s.dat", ZRW_DIR, plist[i].ID);
        if((zrw_file=fopen(zrw_filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s \n", zrw_filename);
            exit(EXIT_FAILURE);
        }
        fscanf(zrw_file, "%d", &N); /* read in number of stars */

        /* Claim arrays */
        Z = calloc(N, sizeof(float));
        R = calloc(N, sizeof(float));
        W = calloc(N, sizeof(float));

        /* Read file for zrw data */
        for(j=0; j<N; j++){
            fscanf(zrw_file, "%f", &Z[j]);
            fscanf(zrw_file, "%f", &R[j]);
            fscanf(zrw_file, "%f", &W[j]);
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
            fscanf(file, "%f", &b[j].DD);
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
            fscanf(file, "%f", &b[j].DD_err_jk);
        }
        fclose(file);

        /* Next load MM errors */
        snprintf(filename, 256, "%suniform_%s_frac_error.dat", ERR_DIR, plist[i].ID);
        if((file=fopen(filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s\n", filename);
            exit(EXIT_FAILURE);
        }
        for(j=0; j<N_bins; j++){
            fscanf(file, "%f", &b[j].MM_err_jk);
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
    fprintf(stderr, "Pairs loaded from %s\n", PAIRS_DIR);


}

/* ----------------------------------------------------------------------- */

/* Load starting data for MCMC loop */
void load_step_data(STEP_DATA *step_data){

    // step_data->N_params = 5;
    // step_data->thin_r0 = 3.0;
    // step_data->thin_z0 = 0.3;
    // step_data->thick_r0 = 4.0;
    // step_data->thin_z0 = 1.2;
    // step_data->ratio_thick_thin = 0.1;
    step_data->thin_r0 = 2.475508;
    step_data->thin_z0 = 0.241209;
    step_data->thick_r0 = 2.417346;
    step_data->thick_z0 = 0.694395;
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
float sech2(float x){
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
                    * exp( -p[i].R[j] / params.thick_r0 ) ) );
        }
    }
}

/* ----------------------------------------------------------------------- */

/* Determine normalization of MM counts */
float normalize_MM(float *weight, int N_stars){

    int i, j;
    float norm = 0.0;

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
float calculate_MM( unsigned int N_pairs, int *pair1, int *pair2,
    float MM_norm, float *weight ){

    unsigned int i;
    float MM = 0.0;

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
    float MM_norm;

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


STEP_DATA update_parameters(STEP_DATA p){

    float delta;

    float thin_r0_sigma = 0.05;
    float thin_z0_sigma = 0.005;
    float thick_r0_sigma = 0.05;
    float thick_z0_sigma = 0.005;
    float ratio_thick_thin_sigma = 0.002;

    const gsl_rng_type * GSL_T;
    gsl_rng * GSL_r;

    gsl_rng_env_setup();

    GSL_T = gsl_rng_default;
    GSL_r = gsl_rng_alloc(GSL_T);

    gsl_rng_set(GSL_r, time(NULL));

    /* change the position based on Gaussian distributions.  */
    delta = gsl_ran_gaussian(GSL_r, thin_r0_sigma);
    p.thin_r0 += delta;

    delta = gsl_ran_gaussian(GSL_r, thin_z0_sigma);
    p.thin_z0 += delta;

    delta = gsl_ran_gaussian(GSL_r, thick_r0_sigma);
    p.thick_r0 += delta;

    delta = gsl_ran_gaussian(GSL_r, thick_z0_sigma);
    p.thick_z0 += delta;

    while(1){
        delta = gsl_ran_gaussian(GSL_r, ratio_thick_thin_sigma);
        p.ratio_thick_thin += delta;
        if(p.ratio_thick_thin < 1.0) break;
    }

    return p;
}


void run_mcmc(STEP_DATA initial_step, int max_steps, int N_plist, POINTING *plist, int N_bins){

    int i;
    // int eff_counter;
    // float eff;
    STEP_DATA current;
    STEP_DATA new;
    float delta_chi2;
    int DOF;
    float tmp;
    int N_params = 5;

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
    DOF -= N_params;
    current.chi2_reduced = current.chi2 / (float)DOF;

    fprintf(stderr, "Degrees of freedom is: %d\n", DOF );

    fprintf(stderr, "Chi2 value for intital params is %f\n", current.chi2);

    for( i = 0; i < max_steps; i++ ){

        new = update_parameters(current);

        set_weights(new, plist, N_plist);
        calculate_correlation(plist, N_plist, N_bins);
        calculate_chi2(plist, &new, N_plist, N_bins);
        new.chi2_reduced = new.chi2 / (float)DOF;

        delta_chi2 = new.chi2 - current.chi2;


        if(delta_chi2 <= 0.0){
            current = new;
        }
        else{
            tmp = (float)rand() / (float)RAND_MAX;
            if (tmp < exp( -delta_chi2 / 2.0 )){
                current = new;
            }
            else{
                /* use old positions */
            }
        }

        // fprintf(stderr, "Current chi2 is %f\n", current.chi2);

    }
    fprintf(stderr, "End MCMC calculation.\n");
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
    int max_steps = 100;
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