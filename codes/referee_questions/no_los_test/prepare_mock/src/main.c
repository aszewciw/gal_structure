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
    PARAMS params;  // parameters for mock creation
    time_t t;       // initialization of random seed

    /* get info for mock */
    /* change this to CL input eventually */
    get_params(&params, N_stars);

    /* Allocate arrays for galactic coordinates */
    STAR * thin  = malloc(params.N_thin * sizeof(STAR));
    STAR * thick = malloc(params.N_thick * sizeof(STAR));

    /* initialize random seed */
    srand((unsigned) time(&t));

    generate_stars(thin, &params, 0);
    generate_stars(thick, &params, 1);

    /* Deallocate arrays */
    free(thin);
    free(thick);
    fprintf(stderr, "Files Written. Arrays deallocated.\n");

    return 0;
}

/*---------------------------------------------------------------------------*/
