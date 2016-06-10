#include "config.h"

/*

See README

*/

/*---------------------------------------------------------------------------*/

int main( int argc, char **argv ){

    /* CL input for total number of stars in each mock */
    if (argc != 2){
        fprintf( stderr, "Error. Usage: %s num_stars\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    /* total number of stars in temp galaxy */
    unsigned long int N_stars;
    sscanf(argv[1], "%lu", &N_stars);
    fprintf(stderr, "%lu stars per temporary galaxy.\n", N_stars);

    /* different variables used in main */
    POINTING *plist;        // a pointing structure
    int N_plist;            // number of l.o.s.
    int loop_flag;          // set = 0 when file creation complete
    int pointings_in_need;  // a progress checker
    PARAMS params;          // parameters for mock creation
    time_t t;               // initialization of random seed
    int N_mock;             // # of stars in current mock l.o.s.
    int N_data;             // desired # of stars in current l.o.s.
    int i;                  // for loop index
    int loop_counter;       // a progress checker

    /* load info for different pointings */
    load_pointing_list(&N_plist, &plist);

    /* get info for mock */
    /* change this to CL input eventually */
    get_params(&params, N_stars);

    /* Allocate arrays for galactic coordinates */
    STAR * pop1  = malloc(params.N_1 * sizeof(STAR));
    STAR * pop2 = malloc(params.N_2 * sizeof(STAR));

    /* initialize random seed */
    srand((unsigned) time(&t));

    /* Initialize for while loop */
    loop_flag    = 0;
    loop_counter = 0;

    /* create temp mocks until all l.o.s. are filled */
    while(loop_flag==0){

        /* re-initialize at each step */
        pointings_in_need = 0;
        loop_flag         = 1;

        /* Make pop1 and pop2 disks */
        generate_stars(pop1, &params, 1);
        generate_stars(pop2, &params, 2);

        /* Separate stars into appropriate l.o.s. */
        separate_sample(plist, pop1, N_plist, params.N_pop1);
        separate_sample(plist, pop2, N_plist, params.N_pop2);

        /* Check all l.o.s. to see if we have enough stars */
        for( i=0; i<N_plist; i++ ){

            N_mock = plist[i].N_mock;
            N_data = plist[i].N_data;

            if(N_mock<N_data){
                /* indicate that we need more stars */
                loop_flag         = 0;
                plist[i].flag     = 0;
                pointings_in_need += 1;
            }
            else{
                /* we don't need more stars for this l.o.s. */
                plist[i].flag = 1;
            }
        }

        /* update progress and output results to user */
        loop_counter +=1;
        fprintf(stderr, "We've run the loop %d times.\n", loop_counter);
        if (pointings_in_need != 0){
            fprintf(stderr, "%d pointings need more stars.\n", pointings_in_need);
            fprintf(stderr, "Making more stars. \n");
        }
        else fprintf(stderr, "All poitings have an adequate number of stars. \n");
    }

    /* Deallocate arrays */
    free(pop1);
    free(pop2);
    free(plist);
    fprintf(stderr, "Files Written. Arrays deallocated.\n");


    return 0;
}

/*---------------------------------------------------------------------------*/
