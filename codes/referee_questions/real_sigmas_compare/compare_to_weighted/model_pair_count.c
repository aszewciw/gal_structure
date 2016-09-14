#include <stdlib.h>
#include <stdio.h>
#include <math.h>

typedef struct POINT{
    double x, y, z, weight;
} POINT;

typedef struct CORRELATION{
    double r_lower, r_upper, r_middle, bin_size;
    double r2_lower, r2_upper;
    // long int DD_N;  raw pair counts
    double DD; /* normalized pair counts */
} CORRELATION;

/* ------------------------------------------------------------------------- */

void pairs( POINT *data, int N_data, CORRELATION *corr, int N_corr ){

    double r1, r2, dx, dy, dz, ds;

    int i, j, k;

    for(i = 0; i < N_data; i++){

        for(j = i + 1; j < N_data; j++){

            dx = data[i].x - data[j].x;
            dy = data[i].y - data[j].y;
            dz = data[i].z - data[j].z;

            ds = dx * dx + dy * dy + dz * dz; /* distance square */

            for(k = 0; k < N_corr; k++ ){

                r1 = corr[k].r2_lower;
                r2 = corr[k].r2_upper;
                if(ds >= r1 && ds < r2){
                    corr[k].DD += weight[i]*weight[j];
                    break;
                }
            }
        }
    }
}

/* ------------------------------------------------------------------------- */

double pairs_norm( POINT *data, int N_data ){

    double total=0.0;
    int i, j;

    for( i=0; i<N_data; i++ ){

        for( j=0; j<N_data; j++ ){

            if(i==j) continue;
            total+=weight[i]*weight[j];
        }
    }

    /* Divide by 2 because of double counting */
    total /= 2.0;
    return total;
}

/* ------------------------------------------------------------------------- */

int main(int argc, char **argv){

    if (argc != 3){
        fprintf( stderr, "Usage:\n %s data_file bins_file > outfile\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    FILE *data_file;

    if((data_file=fopen(argv[1],"r"))==NULL){
        fprintf(stderr,"Error: Cannot open file %s \n", argv[1]);
        exit(EXIT_FAILURE);
    }

      FILE *bins_file;

    if((bins_file=fopen(argv[2],"r"))==NULL){
        fprintf(stderr,"Error: Cannot open file %s \n", argv[1]);
        exit(EXIT_FAILURE);
    }

    int nbins;
    fscanf(bins_file, "%d", &nbins);

    CORRELATION *corr;
    corr = calloc(nbins, sizeof(CORRELATION));

    int i, k;

    /*  read in bin settings and prepare corr */
    for(k = 0; k < nbins; k++){
        fscanf(bins_file, "%lf", &corr[k].r_lower);
        fscanf(bins_file, "%lf", &corr[k].r_upper);
        fscanf(bins_file, "%lf", &corr[k].r_middle);
        fscanf(bins_file, "%lf", &corr[k].bin_size);
        corr[k].r2_lower = corr[k].r_lower * corr[k].r_lower;
        corr[k].r2_upper = corr[k].r_upper * corr[k].r_upper;
        corr[k].DD_N = 0; //raw pair counts
        corr[k].DD = 0.0; //normalized pair counts
    }


    /* load data file */
    int N_data;
    POINT *data;

    fprintf(stderr, "data file is: %s\n", argv[1]);
    fprintf(stderr, "Reading data .. \n");

    fscanf(data_file, "%d", &N_data); /* first read in the length of the list */

    /* Claim an array for a list of pointing */
    data = calloc(N_data, sizeof(POINT));

    for(i = 0; i < N_data; i++){
        fscanf(data_file, "%lf", &data[i].x);
        fscanf(data_file, "%lf", &data[i].y);
        fscanf(data_file, "%lf", &data[i].z);
        fscanf(data_file, "%lf", &data[i].weight);
    }

    fprintf(stderr, "Read %d stars. \n", N_data);

    fclose(data_file);

    /* calculate the correlation */
    fprintf(stderr, "Start calculating mock pair counts... \n");

    double normalization = pairs_norm(data, N_data);
    pairs(data, N_data, corr, nbins);


    /* output */
    for(k = 0; k < nbins; k++){

        corr[k].DD = corr[k].DD / normalization;
        // fprintf(stdout, "%lf\t%lf\t%lf\t%lf\t%ld\t%le\n",
        //     corr[k].r_lower, corr[k].r_upper, corr[k].r_middle, corr[k].bin_size,
        //     corr[k].DD_N, corr[k].DD);
        fprintf( stdout, "%le\n", corr[k].DD );
    }

    fprintf(stderr, "Done calculation and output. \n");


    return EXIT_SUCCESS;

}
