#include "mcmc.h"


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
                ( sech2( p[i].Z[j] / (2.0 * params.thin_z0) )
                    * exp( -p[i].R[j] / params.thin_r0 ) )
                + params.ratio_thick_thin *
                ( sech2( p[i].Z[j] / (2.0 * params.thick_z0) )
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

    // double thin_r0_sigma = 0.05;
    // double thin_z0_sigma = 0.005;
    // double thick_r0_sigma = 0.05;
    // double thick_z0_sigma = 0.005;
    // double ratio_thick_thin_sigma = 0.002;

    /* try alternate step sizes */
    double thin_r0_sigma = 0.2;
    double thin_z0_sigma = 0.01;
    double thick_r0_sigma = 0.25;
    double thick_z0_sigma = 0.025;
    double ratio_thick_thin_sigma = 0.05;

    /* change the position based on Gaussian distributions.  */
    delta = gsl_ran_gaussian(GSL_r, thin_r0_sigma);
    p_new.thin_r0 = p.thin_r0 + delta;

    delta = gsl_ran_gaussian(GSL_r, thin_z0_sigma);
    p_new.thin_z0 = p.thin_z0 + delta;

    delta = gsl_ran_gaussian(GSL_r, thick_r0_sigma);
    p_new.thick_r0 = p.thick_r0 + delta;

    delta = gsl_ran_gaussian(GSL_r, thick_z0_sigma);
    p_new.thick_z0 = p.thick_z0 + delta;

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
void run_mcmc(POINTING *plist, STEP_DATA initial, int N_bins, int max_steps,
    int lower_ind, int upper_ind, int rank, int nprocs)
{
    int i;
    int eff_counter = 0; // number of accepted steps
    double eff; // number accepted / total
    STEP_DATA current;
    STEP_DATA new; // mcmc parameters to test
    double delta_chi2, tmp;
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
            if(i % 1000 == 0){
                fprintf(stderr, "On step %d, accepted chi2 is %lf\n",
                    i, current.chi2);
            }
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

