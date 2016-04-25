#include "mcmc.h"

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
    if(rank == 0)fprintf(stderr, "Pairs loaded from %s\n", PAIRS_DIR);
}

/* ----------------------------------------------------------------------- */

/* Load starting data for MCMC loop */
void load_step_data(STEP_DATA *step_data){

    step_data->thin_r0 = 3.0;
    step_data->thin_z0 = 0.3;
    step_data->thick_r0 = 4.0;
    step_data->thick_z0 = 1.2;
    step_data->ratio_thick_thin = 0.1;
}

/* ----------------------------------------------------------------------- */


/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* ------------------  Functions calculating errors  --------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */

/* ----------------------------------------------------------------------- */

/* Calculate fractional error in correlation */
void calculate_frac_error(POINTING *p, int N_bins, int lower_ind, int upper_ind){

    int i, j;

    for(i = lower_ind; i < upper_ind; i++){

        for(j = 0; j < N_bins; j++){

            /* Multiply this by (DD/MM)**2 to get sigma**2 */
            p[i].rbin[j].err2_frac = (
                p[i].rbin[j].DD_err_jk * p[i].rbin[j].DD_err_jk
                + p[i].rbin[j].MM_err_jk * p[i].rbin[j].MM_err_jk );
        }
    }
}

/* ----------------------------------------------------------------------- */

/* Calculate chi2 for a process's given slice of pointings */
double calculate_chi2(POINTING *p, int N_bins, int lower_ind, int upper_ind){

    int i, j;
    double chi2 = 0.0; //initialize

    for(i = lower_ind; i < upper_ind; i++){

        for(j = 0; j < N_bins; j++){

            /* multiplying by fractional error */
            p[i].rbin[j].sigma2 = ( p[i].rbin[j].corr * p[i].rbin[j].corr *
                p[i].rbin[j].err2_frac );

            /* ignore lines of sight with 0 counts */
            if( p[i].rbin[j].sigma2 == 0.0 ) continue;

            chi2 += ( ( p[i].rbin[j].corr - 1.0 ) * ( p[i].rbin[j].corr - 1.0 )
                / p[i].rbin[j].sigma2 );
        }
    }

    return chi2;
}


/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* -------------------  Functions called by MCMC  ------------------------ */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */

/* ----------------------------------------------------------------------- */

/* function used to set density weights */
double sech2(double x){
    return 1.0 / (cosh(x) * cosh(x));
}

/* ----------------------------------------------------------------------- */

/* Set weights for all model points based on disk parameters */
void set_weights(STEP_DATA params, POINTING *p, int lower_ind, int upper_ind){

    int i, j;

    for(i = lower_ind; i < upper_ind; i++){

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
void calculate_correlation(POINTING *p, int N_bins, int lower_ind, int upper_ind){

    int i, j;
    double MM_norm;

    /* Loop over l.o.s. */
    for(i = lower_ind; i < upper_ind; i++){

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

/* Calculate degrees of freedom -- only do once */
int degrees_of_freedom(POINTING *p, int N_bins, int lower_ind, int upper_ind){
    int dof = 0;
    int i, j;

    for(i = lower_ind; i < upper_ind; i++){

        for(j = 0; j < N_bins; j++){

            if( p[i].rbin[j].sigma2 == 0.0 ) continue;

            dof++;
        }
    }

    return dof;
}

/* ----------------------------------------------------------------------- */

/* Take a random step in parameter space */
STEP_DATA update_parameters(STEP_DATA p, gsl_rng * GSL_r){

    double delta;
    STEP_DATA p_new;

    double thin_r0_sigma = 0.05;
    double thin_z0_sigma = 0.005;
    double thick_r0_sigma = 0.05;
    double thick_z0_sigma = 0.005;
    double ratio_thick_thin_sigma = 0.002;

    /* change the position based on Gaussian distributions.  */
    delta = gsl_ran_gaussian(GSL_r, thin_r0_sigma);
    p_new.thin_r0 = p.thin_r0 + delta;

    delta = gsl_ran_gaussian(GSL_r, thin_z0_sigma);
    p_new.thin_z0 = p.thin_z0 + delta;

    delta = gsl_ran_gaussian(GSL_r, thick_r0_sigma);
    p_new.thick_r0 = p.thick_r0 + delta;

    delta = gsl_ran_gaussian(GSL_r, thick_z0_sigma);
    p_new.thick_z0 = p.thick_z0 + delta;

    while(1){
        delta = gsl_ran_gaussian(GSL_r, ratio_thick_thin_sigma);
        p_new.ratio_thick_thin = p.ratio_thick_thin + delta;
        if(p_new.ratio_thick_thin < 1.0) break;
    }

    /* Initialize chi2 values to 0 instead of nonsense */
    p_new.chi2 = 0.0;
    p_new.chi2_reduced = 0.0;

    return p_new;
}

/* ----------------------------------------------------------------------- */

/* Output mcmc data to a file */
void output_mcmc(int index, STEP_DATA p, FILE *output_file){

    fprintf( output_file, "%d\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\n",
        index, p.chi2, p.chi2_reduced, p.thin_r0, p.thin_z0,
        p.thick_r0, p.thick_z0, p.ratio_thick_thin );
}

/* ----------------------------------------------------------------------- */

/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* -------------------------------- MCMC --------------------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */

/* Run mcmc chain */
void run_mcmc(POINTING *plist, STEP_DATA initial, int N_bins, int max_steps,
    int lower_ind, int upper_ind, int rank, int nprocs)
{
    int i;
    int eff_counter = 0; // number of accepted steps
    double eff; // number accepted / total
    STEP_DATA current;
    STEP_DATA new; // mcmc parameters to test
    double delta_chi2, temp;
    int DOF = 0; // total degrees of freedom
    int DOF_proc; // d.o.f. of each process
    int N_params = 5; // number of parameters -- should automate this
    double chi2 = 0.0;

    if (rank == 0){
        fprintf(stderr, "Start MCMC chain. Max steps = %d\n", max_steps);
    }

    /* set first element with initial parameters */
    current = initial;

    /* set initial weights of model points */
    set_weights(current, plist, lower_ind, upper_ind);
    if(rank==0) fprintf(stderr, "Initial weights set \n");

    /* Calculate initial correlation value */
    calculate_correlation(plist, N_bins, lower_ind, upper_ind);
    chi2 = calculate_chi2(plist, N_bins, lower_ind, upper_ind);
    MPI_Allreduce(&chi2, &current.chi2, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);

    /* Degrees of freedom never change -- calculate once */
    DOF_proc = degrees_of_freedom(plist, N_bins, lower_ind, upper_ind);
    MPI_Allreduce(&DOF_proc, &DOF, 1, MPI_INT, MPI_SUM, MPI_COMM_WORLD);
    DOF -= N_params;
    current.chi2_reduced = current.chi2 / (double)DOF;

    if(rank==0){
        fprintf(stderr, "Degrees of freedom is: %d\n", DOF);
        fprintf(stderr, "Chi2 value for intital params is %lf\n", current.chi2);
    }
    int current_rank;

    /* Define MPI type to be communicated */
    MPI_Datatype MPI_STEP;
    MPI_Datatype type[7] = { MPI_DOUBLE, MPI_DOUBLE, MPI_DOUBLE, MPI_DOUBLE, MPI_DOUBLE, MPI_DOUBLE, MPI_DOUBLE };
    int blocklen[7] = { 1, 1, 1, 1, 1, 1, 1 };
    MPI_Aint disp[7];
    disp[0] = offsetof( STEP_DATA, thin_r0 );
    disp[1] = offsetof( STEP_DATA, thin_z0 );
    disp[2] = offsetof( STEP_DATA, thick_r0 );
    disp[3] = offsetof( STEP_DATA, thick_z0 );
    disp[4] = offsetof( STEP_DATA, ratio_thick_thin );
    disp[5] = offsetof( STEP_DATA, chi2 );
    disp[6] = offsetof( STEP_DATA, chi2_reduced );

    /* build derived data type */
    MPI_Type_create_struct( 7, blocklen, disp, type, &MPI_STEP );
    /* optimize memory layout of derived datatype */
    MPI_Type_commit(&MPI_STEP);

    /* define file for output and have proc 0 open */
    char output_filename[256];
    FILE *output_file;
    snprintf(output_filename, 256, "%smcmc_result.dat", OUT_DIR);
    if(rank==0){
        output_file = fopen(output_filename, "a");
    }

    /* Initialize random number to be used in MCMC */
    const gsl_rng_type * GSL_T;
    gsl_rng * GSL_r;
    gsl_rng_env_setup();
    GSL_T = gsl_rng_default;
    GSL_r = gsl_rng_alloc(GSL_T);
    gsl_rng_set(GSL_r, time(NULL));


    for( i = 0; i < max_steps; i++ ){

        /* Have only step 0 take random walk and send new params to all procs */

        if(rank==0 && i!=0) new = update_parameters(current, GSL_r);
        MPI_Bcast(&new, 1, MPI_STEP, 0, MPI_COMM_WORLD);

        /* Set weights from new parameters */
        set_weights(new, plist, lower_ind, upper_ind);
        calculate_correlation(plist, N_bins, lower_ind, upper_ind);

        /* Calculate and gather chi2 */
        chi2 = calculate_chi2(plist, N_bins, lower_ind, upper_ind);
        MPI_Allreduce(&chi2, &new.chi2, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
        new.chi2_reduced = new.chi2 / (double)DOF;

        /* If new chi2 is better, accept step.
           If not, decide to accept/reject with some probability */
        /* Only rank 0 needs to do this */
        if(rank == 0){

            delta_chi2 = new.chi2 - current.chi2;

            if(delta_chi2 <= 0.0){
                current = new;
                eff_counter += 1;
            }
            else{
                tmp = (double)rand() / (double)RAND_MAX;
                if (tmp < exp( -delta_chi2 / 2.0 )){
                    current = new;
                    eff_counter += 1;
                }
                else{
                    /* use old positions */
                }
            }
            fprintf(stderr, "On step %d, accepted chi2 is %lf\n", i, current.chi2);
            output_mcmc(i, current, output_file);
            if(i % 50 == 0) fflush(output_file);
        }

    }
    if(rank==0){
        eff = (double)eff_counter / (double)max_steps;
        fclose(output_file);
        fprintf(stderr, "Efficiency of MCMC: %lf\n", eff);
        fprintf(stderr, "End MCMC calculation.\n");
    }

}


/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* -------------------------------- MAIN --------------------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */

/* Test loading of data */
int main(int argc, char * argv[]){

    /* MPI Initialization */
    int nprocs, rank;
    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    if (argc!=1){
        fprintf(stderr, "Usage: %s\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    /* -- Load data from various files --*/
    int i, j;
    int N_plist;
    int N_bins = 12;
    POINTING *plist;

    /* have each process separately access this file */
    int current_rank = 0;
    while ( current_rank < nprocs ){
        if (current_rank == rank) {
            load_pointingID(&N_plist, &plist);
            // fprintf(stderr, "Rank %d has loaded pointing IDs.\n", rank);
            if(rank == 0) fprintf(stderr, "%d pointings to do\n", N_plist);
        }
        MPI_Barrier(MPI_COMM_WORLD); // procs wait here until all arrive
        current_rank++;
    }

    /* Establish slice of pointings for each process to handle */
    int slice_length;
    int remain = N_plist % nprocs;
    int lower_ind, upper_ind;

    slice_length = N_plist / nprocs;
    lower_ind = rank * slice_length;
    if (rank < remain){
        lower_ind += rank;
        slice_length++;
    }
    else lower_ind += remain;
    upper_ind = lower_ind + slice_length;

    /* Each process now loads data for its slice only */
    load_ZRW(plist, lower_ind, upper_ind, rank);
    load_rbins(plist, N_bins, lower_ind, upper_ind, rank);
    load_pairs(plist, N_bins, lower_ind, upper_ind, rank);

    /* Calculate fractional error in DD/MM */
    /* Only must be done once */
    calculate_frac_error(plist, N_bins, lower_ind, upper_ind);

    /* -- Initialize parameters --*/
    STEP_DATA initial;
    load_step_data(&initial);
    if(rank==0) fprintf(stderr, "Default initial parameters set...\n");

    int max_steps = 50;
    run_mcmc(plist, initial, N_bins, max_steps, lower_ind, upper_ind,
        rank, nprocs);

    /* Free allocated values */
    for(i=lower_ind; i<upper_ind; i++){
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
    if(rank==0) fprintf(stderr, "Allocated space cleared. \n");

    /* barrier to ensure all procs clear space before MPI_Finalize */
    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Finalize();

    return EXIT_SUCCESS;

}