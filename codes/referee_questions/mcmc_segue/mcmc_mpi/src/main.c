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

    if (argc!=3){
        fprintf(stderr, "Usage: %s\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    /* number of steps in mcmc */
    int max_steps;
    /* flag to indicate starting parameters */
    int param_flag;

    sscanf(argv[1], "%d", &max_steps);
    sscanf(argv[2], "%d", &param_flag);
    if(rank==0) fprintf(stderr, "%d steps in mcmc chain.\n", max_steps);

    // /* Define MPI type to be communicated */
    // MPI_Datatype MPI_STEP;
    // MPI_Datatype type[7] = { MPI_DOUBLE, MPI_DOUBLE, MPI_DOUBLE, MPI_DOUBLE, MPI_DOUBLE, MPI_DOUBLE, MPI_DOUBLE };
    // int blocklen[7] = { 1, 1, 1, 1, 1, 1, 1 };
    // MPI_Aint disp[7];
    // disp[0] = offsetof( STEP_DATA, thin_r0 );
    // disp[1] = offsetof( STEP_DATA, thin_z0 );
    // disp[2] = offsetof( STEP_DATA, thick_r0 );
    // disp[3] = offsetof( STEP_DATA, thick_z0 );
    // disp[4] = offsetof( STEP_DATA, ratio_thick_thin );
    // disp[5] = offsetof( STEP_DATA, chi2 );
    // disp[6] = offsetof( STEP_DATA, chi2_reduced );

    // /* build derived data type */
    // MPI_Type_create_struct( 7, blocklen, disp, type, &MPI_STEP );
    // /* optimize memory layout of derived datatype */
    // MPI_Type_commit(&MPI_STEP);

    /* -- Initialize parameters --*/
    STEP_DATA initial;
    if(rank==0){
        load_step_data(&initial, param_flag, rank);
    }

    // MPI_Bcast(&initial, 1, MPI_STEP, 0, MPI_COMM_WORLD);

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
            if(rank == 0) fprintf(stderr, "%d pointings to do\n", N_plist);
        }
        MPI_Barrier(MPI_COMM_WORLD);
        current_rank++;
    }

    /* Establish slice of pointings for each process to handle */
    int slice_length;
    int remain = N_plist % nprocs;
    int lower_ind, upper_ind;

    /* Make slices as even as possible */
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

    /* Run mcmc */
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

/* ----------------------------------------------------------------------- */