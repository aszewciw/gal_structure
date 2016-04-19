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

    /* Loop over each pointing */
    for(i=0; i<N_plist; i++){

        /* Claim space for bin data */
        b = calloc(N_bins, sizeof(RBIN));

        /* First load DD counts */
        /* Also assign Bin ID */
        snprintf(filename, 256, "%sdd_%s.dat", DD_DIR, plist[i].ID);
        if((file=fopen(filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s\n", filename);
            exit(EXIT_FAILURE);
        }
        for(j=0; j<N_bins; j++){
            fscanf(file, "%f", &b[j].DD);
            snprintf(&b[j].binID, 256, "%d", j+1);
        }
        fclose(file);

        /* Next load DD errors */
        snprintf(filename, 256, "%sstar_%s_frac_error.dat", ERR_DIR, plist[i].ID);
        if((file=fopen(filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s\n", filename);
            exit(EXIT_FAILURE);
        }
        for(j=0; j<N_bins; j++){
            fscanf(file, "%f", &b[j].DD_err_jk);
        }
        fclose(file);

        /* Next load MM errors */
        snprintf(filename, 256, "%suniform_%s_frac_error.dat", ERR_DIR, plist[i].ID);
        if((file=fopen(filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s\n", filename);
            exit(EXIT_FAILURE);
        }
        for(j=0; j<N_bins; j++){
            fscanf(file, "%f", &b[j].MM_err_jk);
        }
        fclose(file);

        /* Assign values to plist elements */
        plist[i].rbin = b;
    }
    fprintf(stderr, "DD counts loaded from %s\n", DD_DIR);
    fprintf(stderr, "Errors loaded from %s\n", ERR_DIR);
}

/* ----------------------------------------------------------------------- */

/* Load pairs for each bin in each l.o.s. */

void load_pairs(int N_plist, int N_bins, POINTING *plist){

    char pair_filename[256];
    FILE *pair_file;
    int i, j;
    unsigned int k, N;
    unsigned int *pair1;
    unsigned int *pair2;

    /* Loop over each pointing */
    for(i=0; i<N_plist; i++){

        for(j=0; j<N_bins; j++){
            snprintf(pair_filename, 256, "%spairs_%s.bin_%s.dat", PAIRS_DIR, plist[i].ID, plist[i].rbin[j].binID);
            if((pair_file=fopen(pair_filename,"r"))==NULL){
                fprintf(stderr, "Error: Cannot open file %s\n", pair_filename);
                exit(EXIT_FAILURE);
            }

            /* First get number of pairs */
            fscanf(pair_file, "%u", &N);

            /* Claim arrays */
            pair1 = calloc(N, sizeof(unsigned int));
            pair2 = calloc(N, sizeof(unsigned int));

            for(k=0; k<N; k++){
                fscanf(pair_file, "%u", &pair1[k]);
                fscanf(pair_file, "%u", &pair2[k]);
            }

            fclose(pair_file);

            /* Assign values to plist elements */
            plist[i].rbin[j].N_pairs = N;
            plist[i].rbin[j].pair1 = pair1;
            plist[i].rbin[j].pair2 = pair2;
        }

    }
    fprintf(stderr, "Pairs loaded from %s\n", PAIRS_DIR);


}

/* ----------------------------------------------------------------------- */


/* Test loading of data */
int main(int argc, char * argv[]){

    if (argc!=1){
        fprintf(stderr, "Usage: %s\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    int i, j;
    int N_plist;
    int N_bins = 12;
    POINTING *plist;

    load_pointingID(&N_plist, &plist);
    load_ZRW(N_plist, plist);
    load_rbins(N_plist, N_bins, plist);
    load_pairs(N_plist, N_bins, plist);

    fprintf(stderr, "DD count check: %f\n", plist[1].rbin[4].DD);
    fprintf(stderr, "DD error check: %f\n", plist[1].rbin[4].DD_err_jk);
    fprintf(stderr, "MM error check: %f\n", plist[1].rbin[4].MM_err_jk);

    /* Free allocated values */
    for(i=0; i<N_plist; i++){
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

    return EXIT_SUCCESS;

}