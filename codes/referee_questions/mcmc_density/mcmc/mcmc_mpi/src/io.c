#include "mcmc.h"

/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* -----------------------  I / O data functions  ------------------------ */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */


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

    /* First get length of list */
    fscanf(plist_file, "%d", &N);

    /* Claim array for list of pointings */
    p = calloc(N, sizeof(POINTING));

    /* Get pointing IDs */
    int i;
    for(i=0; i<N; i++){
        fscanf(plist_file, "%s", p[i].ID);
    }
    fclose(plist_file);

    /* Assign values to main function arguments */
    *N_plist = N;
    *plist = p;

}

/* ----------------------------------------------------------------------- */

/* Load bin information */
void load_bin_info(int *N_bins){

    char bin_filename[256];
    FILE *bin_file;

    int N;

    snprintf(bin_filename, 256, "%srbins.dat", BIN_DIR);
    if( (bin_file=fopen(bin_filename, "r"))==NULL ){
        fprintf(stderr, "Error: Cannot open file %s \n", bin_filename);
        exit(EXIT_FAILURE);
    }

    /* read in number of bins */
    fscanf(bin_file, "%d", &N);

    fclose(bin_file);

    *N_bins = N;

    // fprintf(stderr, "Bin information loaded. Using %d bins\n", N);
}

/* ----------------------------------------------------------------------- */

/* Read mock density and error values */
void load_mock_data(POINTING *p, int N_bins, int lower_ind, int upper_ind,
    int rank)
{

    char mock_filename[256];
    FILE *mock_file;
    int i, j;
    RBIN *b;

    for(i=lower_ind; i<upper_ind; i++){

        /* reserve space for bin data */
        b = calloc(N_bins, sizeof(RBIN));

        /* check density file */
        snprintf(mock_filename, 256, "%sdensity_%s.dat", DENSITY_DIR,
            p[i].ID);
        if((mock_file=fopen(mock_filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s \n", mock_filename);
            exit(EXIT_FAILURE);
        }

        /* load density data */
        for(j=0; j<N_bins; j++){
            snprintf(b[j].binID, 256, "%d", j);
            fscanf(mock_file, "%lf", &b[j].density_mock);
        }

        fclose(mock_file);

        /* check errors file */
        snprintf(mock_filename, 256, "%serrors_%s.dat", ERROR_DIR,
            p[i].ID);
        if((mock_file=fopen(mock_filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s \n", mock_filename);
            exit(EXIT_FAILURE);
        }

        for(j=0; j<N_bins; j++){
            snprintf(b[j].binID, 256, "%d", j);
            fscanf(mock_file, "%lf", &b[j].density_mock_err);
        }

        fclose(mock_file);

        p[i].rbin = b;
    }

    if(rank==0) fprintf(stderr, "Mock data loaded from %s\n", DENSITY_DIR);
}

/* ----------------------------------------------------------------------- */

/* Load position and density weight data for model stars */
// void load_ZR(int N_p, POINTING *p, int N_bins){
void load_ZR(POINTING *p, int N_bins, int lower_ind, int upper_ind,
    int rank)
{

    char ZR_filename[256];
    FILE *ZR_file;
    int i, j, k, N;
    double * Z;
    double * R;
    double * density;

    /* Read star data for each poiting */
    // for(i = 0; i < N_p; i++){
    for(i = lower_ind; i < upper_ind; i++){

        for(j=0; j<N_bins; j++){

            snprintf( ZR_filename, 256, "%suniform_ZR_%s_bin_%s.dat",
                ZR_DIR, p[i].ID, p[i].rbin[j].binID );
            if((ZR_file=fopen(ZR_filename,"r"))==NULL){
                fprintf(stderr, "Error: Cannot open file %s \n", ZR_filename);
                exit(EXIT_FAILURE);
            }

            fscanf(ZR_file, "%d", &N); /* read in number of stars */

            /* Claim arrays */
            Z       = calloc(N, sizeof(double));
            R       = calloc(N, sizeof(double));
            density = calloc(N, sizeof(double));

            /* Read file for ZR data */
            for(k=0; k<N; k++){
                fscanf(ZR_file, "%lf", &Z[k]);
                fscanf(ZR_file, "%lf", &R[k]);
                density[k]=1.0;
            }

            fclose(ZR_file);

            /* Assign value to p element */
            p[i].rbin[j].N_uniform = N;
            p[i].rbin[j].Z         = Z;
            p[i].rbin[j].R         = R;
            p[i].rbin[j].density   = density;
        }
    }

    if(rank==0) fprintf(stderr, "Model data loaded from %s\n", ZR_DIR);
}

/* ----------------------------------------------------------------------- */

/* Load starting data for MCMC loop */
void load_step_data(STEP_DATA *step_data){

    // step_data->thin_r0          = 3.0;
    // step_data->thin_z0          = 0.3;
    // step_data->thick_r0         = 4.0;
    // step_data->thick_z0         = 1.2;
    // step_data->ratio_thick_thin = 0.1;

    step_data->thin_r0 = 2.34;
    step_data->thin_z0 = 0.233;
    step_data->thick_r0 = 2.51;
    step_data->thick_z0 = 0.674;
    step_data->ratio_thick_thin = 0.1;
}

/* ----------------------------------------------------------------------- */


/* Output mcmc data to a file */
void output_mcmc(int index, STEP_DATA p, FILE *output_file){

    fprintf( output_file, "%d\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\n",
        index, p.chi2, p.chi2_reduced, p.thin_r0, p.thin_z0,
        p.thick_r0, p.thick_z0, p.ratio_thick_thin );
}

/* ----------------------------------------------------------------------- */
