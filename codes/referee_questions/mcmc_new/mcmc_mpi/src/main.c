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

    /* parse command line for starting params, steps, and filename */
    ARGS cl = parse_command_line( argc, argv );

    if(rank==0){
        fprintf(stderr, "N_parameters: %d\n", cl.N_params);
        fprintf(stderr, "Starting parameters: r0_thin = %lf , z0_thin = %lf , \
            r0_thick = %lf , z0_thick = %lf , ratio = %lf\n",
            cl.r0_thin, cl.z0_thin, cl.r0_thick, cl.z0_thick, cl.ratio);
        fprintf(stderr, "%d steps in MCMC chain...\n", cl.max_steps);
        fprintf(stderr, "Results will be output to %s\n", cl.filename);
    }

    /* Assign cl arguments to initial parameters */
    STEP_DATA initial;
    initial.r0_thin = cl.r0_thin;
    initial.z0_thin = cl.z0_thin;
    initial.r0_thick = cl.r0_thick;
    initial.z0_thick = cl.z0_thick;
    initial.ratio_thick_thin = cl.ratio;
    initial.chi2 = 0.0;
    initial.chi2_reduced = 0.0;

    /* -- Load data from various files --*/
    int i, j;
    int N_plist;
    int N_bins;
    POINTING *plist;

    /* have each process separately access these files */
    int current_rank = 0;
    while ( current_rank < nprocs ){
        if (current_rank == rank){
            load_pointingID(&N_plist, &plist);
            if(rank == 0) fprintf(stderr, "%d pointings to do\n", N_plist);
            N_bins = load_Nbins();
            if(rank == 0) fprintf(stderr, "%d bins per pointing\n", N_bins);
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

    /* Run mcmc */
    run_mcmc(plist, cl.N_params, initial, N_bins, cl.max_steps, lower_ind, upper_ind,
        rank, nprocs, cl.filename);

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