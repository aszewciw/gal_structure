#include "mcmc.h"

// /* Parse command line for info on how to run chain */
// args parse_command_line(const int n_args, char ** arg_array)
// {

//    /* defaults */
//    args cl_args;
//    cl_args.min_steps = 0;
//    cl_args.max_steps = 500000;
//    cl_args.params    = 1;
//    cl_args.filename  = "mcmc_result.dat"

//    // cl_args.N = 100;
//    // cl_args.n_timesteps = 10000;
//    // cl_args.xyz_freq = 100;
//    // cl_args.thermo_freq = 100;

//    int cnt = 1;
//    while ( cnt < n_args )
//    {

//       if ( !strcmp(arg_array[cnt],"-min") )
//          cl_args.N = check_arg_sane( arg_array,++cnt,n_args );
//       else if ( !strcmp(arg_array[cnt],"-max") )
//          cl_args.n_timesteps = check_arg_sane( arg_array,++cnt,n_args );
//       else if ( !strcmp(arg_array[cnt],"-p") )
//          cl_args.xyz_freq = check_arg_sane( arg_array,++cnt,n_args );
//       else if ( !strcmp(arg_array[cnt],"-fn") )
//          cl_args.thermo_freq = check_arg_sane( arg_array,++cnt,n_args );
//       else if ( !strcmp(arg_array[cnt],"--help") || !strcmp(arg_array[cnt],"-h") ) {
//          printf("Usage: ./run_md [-N <n_particles>] [-ts <n_timesteps>] [-xyz <xyz_file_output_frequency>] [-o <thermo_output_frequency>]\n");
//          printf("Defaults:\nn_particles: 100\nn_timesteps: 10000\nxyz_file_output_fequency: 100\nthermo_output_frequency: 100\n");
//          exit(-1);
//       }
//       else {
//          printf("\n***Error: Unrecognized CL option: %s\n\n",arg_array[cnt]);
//          printf("Usage: ./run_md [-N <n_particles>] [-ts <n_timesteps>] [-xyz <xyz_file_output_frequency>] [-o <thermo_output_frequency>]\n");
//          printf("Defaults:\nn_particles: 100\nn_timesteps: 10000\nxyz_file_output_fequency: 100\nthermo_output_frequency: 100\n");
//          exit(-1);
//       }
//       cnt++;

//    }

//    printf("=======Command line arguments=======\n");
//    printf("N_atoms: %d\n",cl_args.N);
//    printf("n_timesteps: %d\n",cl_args.n_timesteps);
//    printf("xyz_file_output_frequency: %d\n",cl_args.xyz_freq);
//    printf("thermo_output_frequency: %d\n",cl_args.thermo_freq);
//    printf("====================================\n");

//    return cl_args;

// }



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

    if (argc!=4){
        fprintf(stderr, "Usage: %s\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    /* number of steps in mcmc */
    int max_steps;
    /* flag to indicate starting parameters */
    int param_flag;
    /* name of file to output -- not including path */
    char file_string[256];

    sscanf(argv[1], "%d", &max_steps);
    sscanf(argv[2], "%d", &param_flag);
    if(rank==0) fprintf(stderr, "%d steps in mcmc chain.\n", max_steps);
    sscanf(argv[3], "%s", file_string);

    /* -- Initialize parameters --*/
    STEP_DATA initial;
    load_step_data(&initial, param_flag, rank);

    /* -- Load data from various files --*/
    int i, j;
    int N_plist;
    int N_bins;
    POINTING *plist;

    /* have each process separately access these files */
    int current_rank = 0;
    while ( current_rank < nprocs ){
        if (current_rank == rank) {
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
    load_covariance(plist, N_bins, lower_ind, upper_ind, rank);
    load_correlation(plist, N_bins, lower_ind, upper_ind, rank);

    /* test loading of covariance */
    // if(rank==0){
    //     for(i=0; i<N_bins; i++){
    //         for(j=0; j<N_bins; j++){
    //             fprintf(stderr, "Value: %le, Row: %d, Col: %d \n",
    //                 plist[1].cov_row[i].cov_col[j], i, j);
    //         }
    //     }

    // }
    // MPI_Barrier(MPI_COMM_WORLD);

    /* Calculate DD/RR */
    /* Only must be done once */
    calculate_DD_RR(plist, N_bins, lower_ind, upper_ind);

    /* Run mcmc */
    run_mcmc(plist, initial, N_bins, max_steps, lower_ind, upper_ind,
        rank, nprocs, file_string);

    /* Free allocated values */
    for(i=lower_ind; i<upper_ind; i++){
        for(j=0; j<N_bins; j++){
            free(plist[i].rbin[j].pair1);
            free(plist[i].rbin[j].pair2);
            free(plist[i].cov_row[j].cov_col);
            free(plist[i].cor_row[j].cor_col);
        }
        free(plist[i].rbin);
        free(plist[i].cov_row);
        free(plist[i].cor_row);
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