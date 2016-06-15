#include "mcmc.h"

/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* -------------------------------- MAIN --------------------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */

int main(int argc, char * argv[]){

    if (argc!=2){
        fprintf(stderr, "Usage: %s\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    /* number of steps in mcmc */
    int max_steps;
    sscanf(argv[1], "%d", &max_steps);
    fprintf(stderr, "%d steps in mcmc chain.\n", max_steps);

    /* -- Load data from various files --*/
    int i, j;
    int N_bins = 12;
    MODEL model;

    /* load data */
    load_ZR(&model);
    load_rbins(&model, N_bins);
    load_pairs(&model, N_bins);

    /* Calculate fractional error in DD/MM */
    /* Only must be done once */
    calculate_frac_error(&model, N_bins);

    /* -- Initialize parameters --*/
    STEP_DATA initial;
    load_step_data(&initial);
    fprintf(stderr, "Default initial parameters set...\n");

    run_mcmc(&model, initial, N_bins, max_steps);

    /* Free allocated values */
    for(j=0; j<N_bins; j++){
        free(model.rbin[j].pair1);
        free(model.rbin[j].pair2);
    }
    free(model.rbin);
    free(model.Z);
    free(model.R);
    free(model.weight);

    // free(model);
    fprintf(stderr, "Allocated space cleared. \n");

    /* barrier to ensure all procs clear space before MPI_Finalize */
    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Finalize();

    return EXIT_SUCCESS;

}

/* ----------------------------------------------------------------------- */