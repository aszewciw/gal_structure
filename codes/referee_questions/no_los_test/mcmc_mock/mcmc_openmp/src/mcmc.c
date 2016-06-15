#include "mcmc.h"
#define CHUNKSIZE 100

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
void set_weights(STEP_DATA params, MODEL *m){

    int j;

    #pragma simd
    for(j = 0; j < m->N_stars; j++){

        m->weight[j] = (
            ( sech2( m->Z[j] / (2.0 * params.thin_z0) )
                * exp( -m->R[j] / params.thin_r0 ) )
            + params.ratio_thick_thin *
            ( sech2( m->Z[j] / (2.0 * params.thick_z0) )
                * exp( -m->R[j] / params.thick_r0 ) ) );
    }
}

/* ----------------------------------------------------------------------- */

/* Determine normalization of MM counts */
double normalize_MM(double *weight, int N_stars){

    int i, j;
    double norm = 0.0;
    double norm_private;
    // int chunk = CHUNKSIZE;

    #pragma omp parallel default(shared) private(norm_private, i, j)
    {
        norm_private = 0.0;

        #pragma omp for schedule(guided)
        for(i = 0; i < N_stars; i++){

            for(j = 0; j < N_stars; j++){

                if(i == j) continue;

                norm_private += weight[i] * weight[j];
            }   /* end inner for */

        }   /* end outer for */

        #pragma omp critical
        {
            norm += norm_private;
        } /* end critical section */

    }   /* end parallel section */


    norm /= 2.0;
    return norm;
}

/* ----------------------------------------------------------------------- */

/* Calculate normalized model pair counts MM for 1 bin */
double calculate_MM( unsigned int N_pairs, int *pair1, int *pair2,
    double MM_norm, double *weight )
{

    unsigned int i;
    // int chunk = CHUNKSIZE;
    double MM = 0.0;
    double MM_private;

    #pragma omp parallel default(shared) private(MM_private, i)
    {
        #pragma omp for schedule(guided)
        for(i = 0; i < N_pairs; i++){
            MM_private += weight[pair1[i]] * weight[pair2[i]];
        }   /* end for */

        #pragma omp critical
        {
            MM += MM_private;
        }   /* end critical section */
    }   /* end parallel section */

    MM /= MM_norm;

    return MM;
}

/* ----------------------------------------------------------------------- */

/* Calculates DD/MM for each bin */
void calculate_correlation(MODEL *m, int N_bins){

    double MM_norm;
    int i;

    for(i=0; i<N_bins; i++){

        MM_norm = normalize_MM(m->weight, m->N_stars);

        m->rbin[i].MM = calculate_MM( m->rbin[i].N_pairs,
            m->rbin[i].pair1, m->rbin[i].pair2, MM_norm,
            m->weight );

        if( m->rbin[i].DD == 0.0 || m->rbin[i].MM == 0.0 ){
            m->rbin[i].corr = 0.0;
        }
        else{
            m->rbin[i].corr = m->rbin[i].DD / m->rbin[i].MM;
        }
    }
}

/* ----------------------------------------------------------------------- */

/* Calculate degrees of freedom -- only do once */
int degrees_of_freedom(MODEL *m, int N_bins){

    int dof = 0;
    int j;

    for(j = 0; j < N_bins; j++){

        if( m->rbin[j].DD_err_jk == 0.0 ) continue;
        if( m->rbin[j].MM_err_jk == 0.0 ) continue;
        if( m->rbin[j].DD == 0.0) continue;

        dof++;
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

    /* try alternate step sizes */
    // double thin_r0_sigma = 0.2;
    // double thin_z0_sigma = 0.01;
    // double thick_r0_sigma = 0.25;
    // double thick_z0_sigma = 0.025;
    // double ratio_thick_thin_sigma = 0.05;

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
void run_mcmc(MODEL *model, STEP_DATA initial, int N_bins, int max_steps){

    int i;
    int eff_counter = 0;    /* number of accepted steps */
    double eff;             /* number accepted / total */
    STEP_DATA current;      /* current set of parameters */
    STEP_DATA new;          /* new parameters to test */
    double delta_chi2, tmp; /*  */
    int DOF = 0;            /* total degrees of freedom */
    int N_params = 5;       /* number of parameters */

    fprintf(stderr, "Start MCMC chain. Max steps = %d\n", max_steps);

    /* set current element with initial parameters */
    current = initial;

    /* set initial weights of model points */
    set_weights(current, model);
    fprintf(stderr, "Initial weights set \n");

    /* Calculate initial correlation value */
    calculate_correlation(model, N_bins);
    current.chi2 = calculate_chi2(model, N_bins);

    /* Degrees of freedom never change -- calculate once */
    DOF = degrees_of_freedom(model, N_bins);
    DOF -= N_params;
    current.chi2_reduced = current.chi2 / (double)DOF;

    fprintf(stderr, "Degrees of freedom is: %d\n", DOF);
    fprintf(stderr, "Chi2 value for intital parameters is %lf\n",
        current.chi2);

    /* define file for output and have proc 0 open */
    char output_filename[256];
    FILE *output_file;
    snprintf(output_filename, 256, "%smcmc_result.dat", OUT_DIR);
    output_file = fopen(output_filename, "a");

    /* Initialize random number to be used in MCMC */
    const gsl_rng_type * GSL_T;
    gsl_rng * GSL_r;
    gsl_rng_env_setup();
    GSL_T = gsl_rng_default;
    GSL_r = gsl_rng_alloc(GSL_T);
    gsl_rng_set(GSL_r, time(NULL));

    for( i = 0; i < max_steps; i++ ){

        /* Have only step 0 take random walk and send new params to all procs */
        if(i!=0) new = update_parameters(current, GSL_r);

        /* Set weights from new parameters */
        set_weights(new, model);
        calculate_correlation(model, N_bins);

        /* Calculate and gather chi2 */
        new.chi2 = calculate_chi2(model, N_bins);
        new.chi2_reduced = new.chi2 / (double)DOF;

        /* If new chi2 is better, accept step.
           If not, decide to accept/reject with some probability */
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
        // if(i % 1000 == 0){
        fprintf(stderr, "On step %d, accepted chi2 is %lf\n",
            i, current.chi2);
        // }
        output_mcmc(i, current, output_file);
        if(i % 50 == 0) fflush(output_file);

    }
    eff = (double)eff_counter / (double)max_steps;
    fclose(output_file);
    fprintf(stderr, "Efficiency of MCMC: %lf\n", eff);
    fprintf(stderr, "End MCMC calculation.\n");
}

