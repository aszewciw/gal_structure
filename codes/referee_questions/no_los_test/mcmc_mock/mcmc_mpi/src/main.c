#include "mcmc.h"

/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* -------------------------------- MAIN --------------------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */

int main(int argc, char * argv[]){

    /* MPI Initialization */
    int nprocs, rank;
    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    if (argc!=2){
        fprintf(stderr, "Usage: %s\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    /* number of steps in mcmc */
    int max_steps;
    sscanf(argv[1], "%d", &max_steps);
    if(rank==0) fprintf(stderr, "%d steps in mcmc chain.\n", max_steps);

    /* -- Load data from various files --*/
    int i, j;
    int N_bins = 12;
    MODEL *model;

    if(nprocs!=N_bins){
        fprintf(stderr, "Please use 12 procs!\n");
        exit(EXIT_FAILURE);
    }
    /* have each process separately access these files */
    int current_rank = 0;
    while(current_rank < nprocs){
        if(current_rank==rank){
            load_ZR(model, rank);
            load_rbins(model, N_bins, rank);
            MPI_Barrier(MPI_COMM_WORLD);
            current_rank++;
        }
    }

    /* each proc will load the pairs for its bin */
    load_pairs(model, rank);

    /* Calculate fractional error in DD/MM */
    /* Only must be done once */
    calculate_frac_error(model, N_bins);

    /* -- Initialize parameters --*/
    STEP_DATA initial;
    load_step_data(&initial);
    if(rank==0) fprintf(stderr, "Default initial parameters set...\n");

    run_mcmc(model, initial, N_bins, max_steps, rank, nprocs);

    /* Free allocated values */
    for(i=lower_ind; i<upper_ind; i++){
        for(j=0; j<N_bins; j++){
            free(model->rbin[j].pair1);
            free(model->rbin[j].pair2);
        }
        free(model->rbin);
        free(model->Z);
        free(model->R);
        free(model->weight);
    }
    free(model);
    if(rank==0) fprintf(stderr, "Allocated space cleared. \n");

    /* barrier to ensure all procs clear space before MPI_Finalize */
    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Finalize();

    return EXIT_SUCCESS;

}

/* ----------------------------------------------------------------------- */