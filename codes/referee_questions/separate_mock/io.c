#include "config.h"

/* ----------------------------------------------------------------------- */

/* Load info for different SEGUE plate sky positions */
void load_pointing_list(int *N_plist, POINTING **plist){

    char plist_filename[256];
    snprintf(plist_filename, 256, "%stodo_list.ascii.dat", OUT_DIR);

    FILE *plist_file;
    int N;
    POINTING *p;

    if((plist_file=fopen(plist_filename,"r"))==NULL){
        fprintf(stderr,"Error: Cannot open file %s \n", plist_filename);
        exit(EXIT_FAILURE);
    }

    fprintf(stderr, "Read pointing list from %s \n", plist_filename);

    fscanf(plist_file, "%d", &N); /* first read in the length of the list */

    /* Claim an array for a list of pointing */
    p = calloc(N, sizeof(POINTING));

    int i;
    for(i = 0; i < N; i++){
        fscanf(plist_file, "%s", p[i].ID);
        fscanf(plist_file, "%Lf", &p[i].ra_deg);
        fscanf(plist_file, "%Lf", &p[i].dec_deg);
        fscanf(plist_file, "%Lf", &p[i].ra_rad);
        fscanf(plist_file, "%Lf", &p[i].dec_rad);
        fscanf(plist_file, "%Lf", &p[i].galactic_l_rad);
        fscanf(plist_file, "%Lf", &p[i].galactic_b_rad);
        fscanf(plist_file, "%Lf", &p[i].x);
        fscanf(plist_file, "%Lf", &p[i].y);
        fscanf(plist_file, "%Lf", &p[i].z);
        fscanf(plist_file, "%d", &p[i].N_data);
        p[i].N_mock = 0;
    }

    fclose(plist_file);

    /* Assign the value to main function arguments */
    *N_plist = N;
    *plist = p;

    fprintf(stderr, "%d pointings to do.\n", N);
}

/* ----------------------------------------------------------------------- */

/* Load thin stars */
/* Eventually we won't want to do this here. We'll instead write a function
that makes random stars until each l.o.s. has the appropriate number and then
we'll only save those files, not the file of all stars unseparated */
void load_mock_thin(unsigned long int *N_stars, STAR **thin){

    char filename[256];
    snprintf(filename, 256, "%smocktest_thin.dat", DATA_DIR);

    FILE *file;
    unsigned long int N;
    STAR *s;

    if((file=fopen(filename,"r"))==NULL){
        fprintf(stderr,"Error: Cannot open file %s \n", filename);
        exit(EXIT_FAILURE);
    }

    fprintf(stderr, "Read thin mock from %s \n", filename);

    fscanf(file, "%lu", &N); /* first read in number of stars */

    /* Claim an array for a list of stars */
    s = calloc(N, sizeof(STAR));

    unsigned long int i;
    for(i = 0; i < N; i++){
        fscanf(file, "%Lf", &s[i].gal_z);
        fscanf(file, "%Lf", &s[i].gal_r);
        fscanf(file, "%Lf", &s[i].gal_phi);
        fscanf(file, "%Lf", &s[i].gal_l_rad);
        fscanf(file, "%Lf", &s[i].gal_b_rad);
        fscanf(file, "%Lf", &s[i].ra_rad);
        fscanf(file, "%Lf", &s[i].dec_rad);
        fscanf(file, "%Lf", &s[i].distance);
        fscanf(file, "%Lf", &s[i].x);
        fscanf(file, "%Lf", &s[i].y);
        fscanf(file, "%Lf", &s[i].z);
    }

    fclose(file);

    /* Assign the value to main function arguments */
    *N_stars = N;
    *thin = s;

    fprintf(stderr, "%lu stars in thin disk.\n", N);
}

/* ----------------------------------------------------------------------- */

/* Load thick stars */
/* Eventually we won't want to do this here. We'll instead write a function
that makes random stars until each l.o.s. has the appropriate number and then
we'll only save those files, not the file of all stars unseparated */
void load_mock_thick(unsigned long int *N_stars, STAR **thick){

    char filename[256];
    snprintf(filename, 256, "%smocktest_thick.dat", DATA_DIR);

    FILE *file;
    unsigned long int N;
    STAR *s;

    if((file=fopen(filename,"r"))==NULL){
        fprintf(stderr,"Error: Cannot open file %s \n", filename);
        exit(EXIT_FAILURE);
    }

    fprintf(stderr, "Read thick mock from %s \n", filename);

    fscanf(file, "%lu", &N); /* first read in number of stars */

    /* Claim an array for a list of stars */
    s = calloc(N, sizeof(STAR));

    unsigned long int i;
    for(i = 0; i < N; i++){
        fscanf(file, "%Lf", &s[i].gal_z);
        fscanf(file, "%Lf", &s[i].gal_r);
        fscanf(file, "%Lf", &s[i].gal_phi);
        fscanf(file, "%Lf", &s[i].gal_l_rad);
        fscanf(file, "%Lf", &s[i].gal_b_rad);
        fscanf(file, "%Lf", &s[i].ra_rad);
        fscanf(file, "%Lf", &s[i].dec_rad);
        fscanf(file, "%Lf", &s[i].distance);
        fscanf(file, "%Lf", &s[i].x);
        fscanf(file, "%Lf", &s[i].y);
        fscanf(file, "%Lf", &s[i].z);
    }

    fclose(file);

    /* Assign the value to main function arguments */
    *N_stars = N;
    *thick = s;

    fprintf(stderr, "%lu stars in thick disk.\n", N);
}