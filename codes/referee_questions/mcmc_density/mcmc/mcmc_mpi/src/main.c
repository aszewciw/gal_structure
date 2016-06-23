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
    int N_plist;
    int N_bins;
    POINTING *plist;

    unsigned long int N_total; // total number of stars in galaxy
    N_total = 30000000;

    /* have each process separately access this file */
    int current_rank = 0;
    while ( current_rank < nprocs ){
        if (current_rank == rank) {
            load_pointingID(&N_plist, &plist);
            load_bin_info(&N_bins);
            fprintf(stderr, "Rank %d has found %d bins.\n", rank, N_bins);
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
    load_mock_data(plist, N_bins, lower_ind, upper_ind, rank);
    load_ZR(plist, N_bins, lower_ind, upper_ind, rank);

    /* Calculate fractional error in DD/MM */
    /* Only must be done once */
    calculate_sigma2(plist, N_bins, lower_ind, upper_ind);

    /* -- Initialize parameters --*/
    STEP_DATA initial;
    load_step_data(&initial);
    normalize_density(&initial, N_total);
    if(rank==0) fprintf(stderr, "Default initial parameters set...\n");

    run_mcmc(plist, initial, N_bins, max_steps, lower_ind, upper_ind,
        rank, nprocs, N_total);

    /* Free allocated values */
    for(i=lower_ind; i<upper_ind; i++){
        for(j=0; j<N_bins; j++){
            free(plist[i].rbin[j].Z);
            free(plist[i].rbin[j].R);
            free(plist[i].rbin[j].density);
        }
        free(plist[i].rbin);
    }
    free(plist);
    if(rank==0) fprintf(stderr, "Allocated space cleared. \n");

    /* barrier to ensure all procs clear space before MPI_Finalize */
    MPI_Barrier(MPI_COMM_WORLD);
    MPI_Finalize();

    return EXIT_SUCCESS;

}

/* ----------------------------------------------------------------------- */