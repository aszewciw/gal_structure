#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>
#include <math.h>
#include <time.h>
#include <string.h>
#include <mpi.h>

int main( int argc, char **argv ){

    /* MPI Initialization */
    int nprocs, rank;
    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &nprocs);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    time_t t;
    srand((unsigned) time(&t) + (1+rank));

    // double proc_rnd = pow((double)rand() / (double)RAND_MAX, rank);
    // srand(proc_rnd);

    double proc_rnd = (double)rand() / (double)RAND_MAX;

    fprintf(stderr, "Process %d has initial random as %lf\n", rank, proc_rnd);
    MPI_Finalize();
    return EXIT_SUCCESS;
}
