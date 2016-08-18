#include "config.h"

/*

Produces a two-disk mock Milky Way sample according to parameters in io.c

Produced are a number of files containing sun-centered cartesian positions
of stars in each SEGUE l.o.s.

Each l.o.s. file has the same number of stars as the corresponding SEGUE
l.o.s.

A single mock is produced with a CL input number of stars. It is
challenging to produce stars in each l.o.s. according to a particular
galaxy prescription so we instead make a temporary galaxy with a CL input
number of stars, assign some of the stars to the appropriate l.o.s., then
re-make galaxies until each l.o.s. has enough stars. Cleaning of the
l.o.s.'s to have the exact number of stars as SEGUE occurs in a separate
file. Importantly, for speed purposes, once we have enough stars in a
particular l.o.s., we no longer attempt to assign stars to that l.o.s.

Note: l.o.s. = "line of sight"; i.e., a SEGUE/SDSS plate/pointing
*/

/*---------------------------------------------------------------------------*/

int main( int argc, char **argv ){

    /* MPI Initialization */
    int nprocs, rank;
    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    /* CL input for total number of stars in each mock */
    if (argc != 3){
        fprintf( stderr, "Error. Usage: %s num_stars\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    unsigned long int N_stars;  /* Number of stars in temp galaxy wedge */
    int mock_num;               /* which mock we're making (1 - 1000) */
    int N_mocks;                /* Number of total mocks */

    sscanf(argv[1], "%lu", &N_stars);
    // sscanf(argv[2], "%d", &mock_num);
    sscanf(argv[2], "%d", &N_mocks);
    if(rank==0){
        // fprintf(stderr, "On mock number %d \n", mock_num);
        fprintf(stderr, "Making %d total mocks.\n", N_mocks);
        fprintf(stderr, "%lu stars per temporary galaxy.\n", N_stars);
    }

    /* have each process only make some stars */
    N_stars /= nprocs;
    if(rank==0) fprintf(stderr, "%d processes each responsible for %lu stars.\n", nprocs, N_stars);

    /* different variables used in main */
    POINTING *plist;        /* a pointing structure */
    int N_plist;            /* number of l.o.s. */
    int loop_flag;          /* set = 0 when file creation complete */
    int pointings_in_need;  /* a progress checker */
    PARAMS params;          /* parameters for mock creation */
    time_t t;               /* initialization of random seed */
    int N_mock;             /* # of stars in current mock l.o.s. */
    int N_mock_temp;
    int N_mock_proc;
    int N_data;             /* desired # of stars in current l.o.s. */
    int i;                  /* for loop index */
    int loop_counter;       /* a progress checker */

    /* have each proc separately load info for different pointings */
    int current_rank = 0;
    while ( current_rank < nprocs ){
        if (current_rank == rank) load_pointing_list(&N_plist, &plist, rank);
        MPI_Barrier(MPI_COMM_WORLD);
        current_rank++;
    }

    /* get info for mock */
    /* change this to CL input eventually */
    get_params(&params, N_stars, rank);

    /* Allocate arrays for galactic coordinates */
    STAR * thin  = malloc(params.N_thin * sizeof(STAR));
    STAR * thick = malloc(params.N_thick * sizeof(STAR));

    /* initialize random seed -- make different for each mock */
    srand((unsigned) time(&t) + (1+rank));


    for(mock_num=0; mock_num<N_mocks; mock_num++){

        if(rank==0) fprintf(stderr, "On mock number %d \n", mock_num);

        /* Initialize for while loop */
        loop_flag    = 0;
        loop_counter = 0;

        /* create temp mocks until all l.o.s. are filled */
        while(loop_flag==0){

            if(rank==0) fprintf(stderr, "Entered while\n");

            /* re-initialize at each step */
            pointings_in_need = 0;
            loop_flag         = 1;

            /* Make thin and thick disks */
            generate_stars(thin, &params, 0);
            if(rank==0) fprintf(stderr, "Got thin positions\n");
            generate_stars(thick, &params, 1);
            if(rank==0) fprintf(stderr, "Got thick positions\n");

            /* Separate stars into appropriate l.o.s. */
            separate_sample(plist, thin, N_plist, params.N_thin, rank, mock_num);
            if(rank==0) fprintf(stderr, "Separated thin\n");
            separate_sample(plist, thick, N_plist, params.N_thick, rank, mock_num);
            if(rank==0) fprintf(stderr, "Separated thick\n");

            /* Check all l.o.s. to see if we have enough stars */
            for( i=0; i<N_plist; i++ ){

                /* set total stars for this temp gxy = 0 */
                N_mock_temp = 0;

                /* current pointings stars/proc */
                N_mock_proc = plist[i].N_mock_proc;

                /* Sum stars across all processes to get pointing's total stars for this temp gxy */
                MPI_Allreduce(&N_mock_proc, &N_mock_temp, 1, MPI_INT, MPI_SUM, MPI_COMM_WORLD);

                /* Add temp galaxy's stars to total */
                plist[i].N_mock += N_mock_temp;
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
            if(rank==0){
                fprintf(stderr, "We've run the loop %d times.\n", loop_counter);
                if (pointings_in_need != 0){
                    fprintf(stderr, "%d pointings need more stars.\n", pointings_in_need);
                    fprintf(stderr, "Making more stars. \n");
                }
                else fprintf(stderr, "All pointings have an adequate number of stars. \n");
            }
        }

        /* reset all pointing flags */
        for( i=0; i<N_plist; i++ ) plist[i].flag=0;
    }

    /* Deallocate arrays */
    free(thin);
    free(thick);
    free(plist);
    if(rank==0) fprintf(stderr, "Files Written. Arrays deallocated.\n");

    MPI_Finalize();

    return 0;
}

/*---------------------------------------------------------------------------*/
