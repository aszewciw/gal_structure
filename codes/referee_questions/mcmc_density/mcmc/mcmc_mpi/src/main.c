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
    int N_plist;
    int N_bins;
    POINTING *plist;

    load_pointingID(&N_plist, &plist);
    load_bin_info(&N_bins);
    load_mock_data(N_plist, plist, N_bins);
    load_ZR(N_plist, plist, N_bins);

    /* Calculate fractional error in DD/MM */
    /* Only must be done once */
    // calculate_frac_error(plist, N_bins, lower_ind, upper_ind);

    /* -- Initialize parameters --*/
    STEP_DATA initial;
    load_step_data(&initial);
    fprintf(stderr, "Default initial parameters set...\n");

    // run_mcmc(plist, initial, N_bins, max_steps, lower_ind, upper_ind,
    //     rank, nprocs);

    /* Free allocated values */
    for(i=0; i<N_plist; i++){
        for(j=0; j<N_bins; j++){
            free(plist[i].rbin[j].Z);
            free(plist[i].rbin[j].R);
            free(plist[i].rbin[j].density);
        }
        free(plist[i].rbin);
    }
    free(plist);
    fprintf(stderr, "Allocated space cleared. \n");

    /* barrier to ensure all procs clear space before MPI_Finalize */

    return EXIT_SUCCESS;

}

/* ----------------------------------------------------------------------- */