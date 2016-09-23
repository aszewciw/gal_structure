#include "mcmc.h"


/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* -------------------  Functions called by MCMC  ------------------------ */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */


/* ----------------------------------------------------------------------- */

/* function used to set density weights */
long double sech2(long double x){
    return 1.0 / (cosh(x) * cosh(x));
}

/* ----------------------------------------------------------------------- */

/* Set weights for all model points based on disk parameters */
void set_weights(STEP_DATA params, POINTING *p, int lower_ind, int upper_ind){

    int i, j;

    for(i = lower_ind; i < upper_ind; i++){

        for(j = 0; j < p[i].N_stars; j++){

            p[i].weight[j] = (
                ( sech2( p[i].Z[j] / (2.0 * params.z0_thin) )
                    * exp( -p[i].R[j] / params.r0_thin ) )
                + params.ratio_thick_thin *
                ( sech2( p[i].Z[j] / (2.0 * params.z0_thick) )
                    * exp( -p[i].R[j] / params.r0_thick ) ) );
        }
    }
}

/* ----------------------------------------------------------------------- */

/* Determine normalization of MM counts */
long double normalize_MM(long double *weight, int N_stars){

    int i, j;
    long double norm = 0.0;

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
long double calculate_MM( unsigned int N_pairs, int *pair1, int *pair2,
    long double MM_norm, long double *weight ){

    unsigned int i;
    long double MM = 0.0;

    for(i = 0; i < N_pairs; i++){

        MM += weight[pair1[i]] * weight[pair2[i]];

    }

    MM /= MM_norm;

    return MM;
}

/* ----------------------------------------------------------------------- */

/* Updates normalized values of MM for current model */
void update_model(POINTING *p, int N_bins, int lower_ind, int upper_ind){

    int i, j;
    long double MM_norm;

    /* Loop over l.o.s. */
    for(i = lower_ind; i < upper_ind; i++){

        MM_norm = normalize_MM(p[i].weight, p[i].N_stars);

        for(j = 0; j < N_bins; j++){

            p[i].rbin[j].MM = calculate_MM( p[i].rbin[j].N_pairs,
                p[i].rbin[j].pair1, p[i].rbin[j].pair2, MM_norm,
                p[i].weight );

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

            if( p[i].rbin[j].frac_error == 0.0 ) continue;

            if( p[i].rbin[j].DD == 0.0 ) continue;

            dof++;
        }
    }

    return dof;
}

/* ----------------------------------------------------------------------- */

/* Take a random step in parameter space */
STEP_DATA update_parameters(STEP_DATA p, gsl_rng * GSL_r){

    long double delta;
    STEP_DATA p_new;

    long double r0_thin_sigma = 0.05;
    long double z0_thin_sigma = 0.005;
    long double r0_thick_sigma = 0.05;
    long double z0_thick_sigma = 0.005;
    long double ratio_thick_thin_sigma = 0.002;

    /* try alternate step sizes */
    // long double r0_thin_sigma = 0.2;
    // long double z0_thin_sigma = 0.01;
    // long double r0_thick_sigma = 0.25;
    // long double z0_thick_sigma = 0.025;
    // long double ratio_thick_thin_sigma = 0.05;

    /* change the position based on Gaussian distributions.  */
    delta = gsl_ran_gaussian(GSL_r, r0_thin_sigma);
    p_new.r0_thin = p.r0_thin + delta;

    delta = gsl_ran_gaussian(GSL_r, z0_thin_sigma);
    p_new.z0_thin = p.z0_thin + delta;

    delta = gsl_ran_gaussian(GSL_r, r0_thick_sigma);
    p_new.r0_thick = p.r0_thick + delta;

    delta = gsl_ran_gaussian(GSL_r, z0_thick_sigma);
    p_new.z0_thick = p.z0_thick + delta;

    /* avoid having ratio > 1 or < 0 */
    while(1){
        delta = gsl_ran_gaussian(GSL_r, ratio_thick_thin_sigma);
        p_new.ratio_thick_thin = p.ratio_thick_thin + delta;
        if(p_new.ratio_thick_thin < 1.0 && p_new.ratio_thick_thin >= 0.0) break;
    }

    /* Initialize chi2 values to 0 instead of nonsense */
    p_new.chi2 = 0.0;
    p_new.chi2_reduced = 0.0;

    return p_new;
}


/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* -------------------------------- MCMC --------------------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */

/* Run mcmc chain */
void run_mcmc(POINTING *plist, int N_params, STEP_DATA initial, int N_bins, int max_steps,
    int lower_ind, int upper_ind, int rank, int nprocs, char filename[256])
{
    int i;                  /* mcmc index */
    int eff_counter = 0;    /* number of accepted steps */
    long double eff;             /* number accepted / total */
    STEP_DATA current;      /* current params */
    STEP_DATA new;          /* new mcmc parameters to test */
    long double delta_chi2;      /* new - old chi2 */
    long double tmp;             /* temp holder */
    int DOF = 0;            /* total degrees of freedom */
    int DOF_proc;           /* d.o.f. of each process */
    long double chi2 = 0.0;      /* chi2 value for each process */

    if (rank == 0){
        fprintf(stderr, "Start MCMC chain. Max steps = %d\n", max_steps);
    }

    /* set first element with initial parameters */
    current = initial;

    /* set initial weights of model points */
    set_weights(current, plist, lower_ind, upper_ind);
    if(rank==0) fprintf(stderr, "Initial weights set \n");

    /* get initial values of MM */
    update_model(plist, N_bins, lower_ind, upper_ind);

    /* Calculate initial correlation value */
    chi2 = calculate_chi2(plist, N_bins, lower_ind, upper_ind);
    MPI_Allreduce(&chi2, &current.chi2, 1, MPI_long double, MPI_SUM, MPI_COMM_WORLD);

    /* Degrees of freedom never change -- calculate once */
    DOF_proc = degrees_of_freedom(plist, N_bins, lower_ind, upper_ind);
    MPI_Allreduce(&DOF_proc, &DOF, 1, MPI_INT, MPI_SUM, MPI_COMM_WORLD);
    DOF -= N_params;
    current.chi2_reduced = current.chi2 / (long double)DOF;

    if(rank==0){
        fprintf(stderr, "Degrees of freedom is: %d\n", DOF);
        fprintf(stderr, "Chi2 value for intital params is %Lf\n", current.chi2);
    }

    /* Define MPI type to be communicated */
    MPI_Datatype MPI_STEP;
    MPI_Datatype type[7] = { MPI_long double, MPI_long double, MPI_long double, MPI_long double, MPI_long double, MPI_long double, MPI_long double };
    int blocklen[7] = { 1, 1, 1, 1, 1, 1, 1 };
    MPI_Aint disp[7];
    disp[0] = offsetof( STEP_DATA, r0_thin );
    disp[1] = offsetof( STEP_DATA, z0_thin );
    disp[2] = offsetof( STEP_DATA, r0_thick );
    disp[3] = offsetof( STEP_DATA, z0_thick );
    disp[4] = offsetof( STEP_DATA, ratio_thick_thin );
    disp[5] = offsetof( STEP_DATA, chi2 );
    disp[6] = offsetof( STEP_DATA, chi2_reduced );

    /* build derived data type */
    MPI_Type_create_struct( 7, blocklen, disp, type, &MPI_STEP );
    /* optimize memory layout of derived datatype */
    MPI_Type_commit(&MPI_STEP);

    /* define file for output and have proc 0 open */
    // char output_filename[256];
    FILE *output_file;
    // snprintf(output_filename, 256, "%s%s", OUT_DIR, file_string);
    if(rank==0){
        output_file = fopen(filename, "a");
    }

    /* Initialize random number to be used in MCMC */
    const gsl_rng_type * GSL_T;
    gsl_rng * GSL_r;
    gsl_rng_env_setup();
    GSL_T = gsl_rng_default;
    GSL_r = gsl_rng_alloc(GSL_T);
    gsl_rng_set(GSL_r, time(NULL));

    /* Here is the mcmc */
    for( i = 0; i < max_steps; i++ ){

        /* Have only step 0 take random walk and send new params to all procs */

        if(rank==0 && i!=0) new = update_parameters(current, GSL_r);
        MPI_Barrier(MPI_COMM_WORLD);
        MPI_Bcast(&new, 1, MPI_STEP, 0, MPI_COMM_WORLD);

        /* Set weights from new parameters */
        set_weights(new, plist, lower_ind, upper_ind);

        /* get new MM values */
        update_model(plist, N_bins, lower_ind, upper_ind);

        /* Calculate and gather chi2 */
        chi2 = calculate_chi2(plist, N_bins, lower_ind, upper_ind);
        MPI_Barrier(MPI_COMM_WORLD);
        MPI_Allreduce(&chi2, &new.chi2, 1, MPI_long double, MPI_SUM, MPI_COMM_WORLD);
        new.chi2_reduced = new.chi2 / (long double)DOF;

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
                tmp = (long double)rand() / (long double)RAND_MAX;
                if (tmp < exp( -delta_chi2 / 2.0 )){
                    current = new;
                    eff_counter += 1;
                }
                else{
                    /* use old positions */
                }
            }
            if(i % 1000 == 0){
                fprintf(stderr, "On step %d, accepted chi2 is %Lf\n",
                    i, current.chi2);
                fprintf(stderr, "z0_thin: %Lf, r0_thin: %Lf, z0_thick: %Lf, r0_thick: %Lf, ratio: %Lf\n",
                    current.z0_thin, current.r0_thin, current.z0_thick,
                    current.r0_thick, current.ratio_thick_thin);
            }
            output_mcmc(i, current, output_file);
            if(i % 50 == 0) fflush(output_file);
        }

    }

    /* print lines indicating end of mcmc */
    if(rank==0){
        eff = (long double)eff_counter / (long double)max_steps;
        fclose(output_file);
        fprintf(stderr, "Efficiency of MCMC: %Lf\n", eff);
        fprintf(stderr, "End MCMC calculation.\n");
    }

}

