#include "io_test.h"


/* ----------------------------------------------------------------------- */
/* Load unique ID of each pointing */
void load_pointingID(int *N_plist, POINTING **plist){

    char plist_filename[256];
    snprintf(plist_filename, 256, "%spointing_ID.dat", RAW_DIR);

    FILE *plist_file;
    int N;
    POINTING *p;

    if((plist_file=fopen(plist_filename,"r"))==NULL){
        fprintf(stderr, "Error: Cannot open file %s \n", plist_filename);
        exit(EXIT_FAILURE);
    }

    fprintf(stderr, "Read pointing list from %s \n", plist_filename);

    fscanf(plist_file, "%d", &N); //length of list

    // Claim array for list of pointings
    p = calloc(N, sizeof(POINTING));

    // Get pointing IDs
    int i;
    for(i=0; i<N; i++){
        fscanf(plist_file, "%s", p[i].ID);
    }
    fclose(plist_file);

    // Aassign values to main function arguments
    *N_plist = N;
    *plist = p;

    fprintf(stderr, "%d pointings to do.\n", N);

}

/* ----------------------------------------------------------------------- */

/* Load position and density weight data for model stars */
void load_ZRW(int N_plist, POINTING *plist){

    char zrw_filename[256];
    FILE *zrw_file;
    int i, j, N;
    float * Z;
    float * R;
    float * W;

    /* Read star data for each poiting */
    for(i=0; i<N_plist; i++){
        snprintf(zrw_filename, 256, "%suniform_ZRW_%s.dat", ZRW_DIR, plist[i].ID);
        if((zrw_file=fopen(zrw_filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s \n", zrw_filename);
            exit(EXIT_FAILURE);
        }
        fscanf(zrw_file, "%d", &N); /* read in number of stars */

        /* Claim arrays */
        Z = calloc(N, sizeof(float));
        R = calloc(N, sizeof(float));
        W = calloc(N, sizeof(float));

        /* Read file for zrw data */
        for(j=0; j<N; j++){
            fscanf(zrw_file, "%f", &Z[j]);
            fscanf(zrw_file, "%f", &R[j]);
            fscanf(zrw_file, "%f", &W[j]);
        }

        fclose(zrw_file);

        /* Assign value to plist element */
        plist[i].N_stars = N;
        plist[i].Z = Z;
        plist[i].R = R;
        plist[i].weight = W;
    }

    fprintf(stderr, "Model data loaded from %s\n", ZRW_DIR);
}

/* ----------------------------------------------------------------------- */

/* Load data for each bin from a variety of files */
void load_rbins(int N_plist, int N_bins, POINTING *plist){

    char filename[256];
    FILE *file;
    int i, j;
    RBIN *b;

    /* Read star data for each pointing */
    for(i=0; i<N_plist; i++){

        /* Claim space for bin data */
        b = calloc(N_bins, sizeof(RBIN));

        /* First load DD counts */
        snprintf(filename, 256, "%sdd_%s.dat", DD_DIR, plist[i].ID);
        if((file=fopen(filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s\n", filename);
            exit(EXIT_FAILURE);
        }
        for(j=0; j<N_bins; j++){
            fscanf(file, "%f", &b.DD[j]);
        }
        fclose(file);

        /* Next load DD errors */
        snprintf(filename, 256, "%sstar_%s_frac_error.dat", ERR_DIR, plist[i].ID);
        if((file=fopen(filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s\n", filename);
            exit(EXIT_FAILURE);
        }
        for(j=0; j<N_bins; j++){
            fscanf(file, "%f", &b.DD_err_jk[j]);
        }
        fclose(file);

        /* Next load MM errors */
        snprintf(filename, 256, "%suniform_%s_frac_error.dat", ERR_DIR, plist[i].ID);
        if((file=fopen(filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s\n", filename);
            exit(EXIT_FAILURE);
        }
        for(j=0; j<N_bins; j++){
            fscanf(file, "%f", &b.MM_err_jk[j]);
        }
        fclose(file);

        /* Assign values to plist elements */
        plist[i].rbin = b;
    }
    fprintf(stderr, "DD counts loaded from %s\n", DD_DIR);
    fprintf(stderr, "Errors loaded from %s\n", ERR_DIR);
}

/* ----------------------------------------------------------------------- */



/* Test loading of data */
int main(int argc, char * argv[]){

    if (argc!=1){
        fprintf(stderr, "Usage: %s\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    int i;
    int N_plist;
    int N_bins = 12;
    POINTING *plist;

    load_pointingID(&N_plist, &plist);
    load_ZRW(N_plist, plist);
    load_rbins(N_plist, N_bins, plist);


    int N_temp = plist[0].N_stars - 1;
    fprintf(stderr, "DD count check: %f\n", plist[1].rbin[4].DD);
    fprintf(stderr, "MM error check: %f\n", plist[1].rbin[4].DD_err_jk);
    fprintf(stderr, "DD error check: %f\n", plist[1].rbin[4].MM_err_jk);

    /* Free allocated values */
    for(i=0; i<N_plist; i++){
        free(plist[i].Z);
        free(plist[i].R);
        free(plist[i].weight);
        free(plist[i].rbin);
    }
    free(plist);

    return EXIT_SUCCESS;

}