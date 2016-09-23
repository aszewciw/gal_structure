#include "mcmc.h"

/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* -----------------------  I / O data functions  ------------------------ */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */


/* ----------------------------------------------------------------------- */

/* check if we passed a filename, number of steps, or parameters */
ARGS parse_command_line( int n_args, char ** arg_array ){

    /* defaults */
    ARGS cl_args;
    cl_args.N_params = 5;
    cl_args.r0_thin = 3.0;
    cl_args.z0_thin = 0.3;
    cl_args.r0_thick = 4.0;
    cl_args.z0_thick = 1.2;
    cl_args.ratio = 0.12;
    strcpy(cl_args.filename, "../data/mcmc_output/mcmc_result.dat");
    cl_args.max_steps = 100000;

    int cnt = 1;
    while(cnt < n_args)
    {
        if ( !strcmp(arg_array[cnt],"-N_p") )
            sscanf(arg_array[++cnt], "%d", &cl_args.N_params);
        else if ( !strcmp(arg_array[cnt],"-rn") )
            sscanf(arg_array[++cnt], "%lf", &cl_args.r0_thin);
        else if ( !strcmp(arg_array[cnt],"-zn") )
            sscanf(arg_array[++cnt], "%lf", &cl_args.z0_thin);
        else if ( !strcmp(arg_array[cnt],"-rk") )
            sscanf(arg_array[++cnt], "%lf", &cl_args.r0_thick);
        else if ( !strcmp(arg_array[cnt],"-zk") )
            sscanf(arg_array[++cnt], "%lf", &cl_args.z0_thick);
        else if ( !strcmp(arg_array[cnt],"-a") )
            sscanf(arg_array[++cnt], "%lf", &cl_args.ratio);
        else if ( !strcmp(arg_array[cnt],"-f") )
            sscanf(arg_array[++cnt], "%s", cl_args.filename);
        else if ( !strcmp(arg_array[cnt],"-N_s") )
            sscanf(arg_array[++cnt], "%d", &cl_args.max_steps);
        else if ( !strcmp(arg_array[cnt],"--help") || !strcmp(arg_array[cnt],"-h") ) {
            printf("Usage: ./run_mcmc [-N_p <n_parameters>] [-rn <r0_thin>] [-zn <z0_thin>] [-rk <r0_thick>] [-zk <z0_thick>] [-f <filename>] [-N_s <max_steps in chain>]\n");
            printf("Defaults:\nN_p: 5\nrn: 2.34\nzn: 0.233\nrk: 2.51\nzk: 0.674\na: 0.1\nf: ../data/mcmc_output/mcmc_result.dat\nN_s=20");
            exit(-1);
        }
        else{
            printf("\n***Error: Uncrecognized CL option %s\n\n", arg_array[cnt]);
            printf("Usage: ./run_mcmc [-N_p <n_parameters>] [-rn <r0_thin>] [-zn <z0_thin>] [-rk <r0_thick>] [-zk <z0_thick>] [-f <filename>] [-N_s <max_steps in chain>]\n");
            printf("Defaults:\nN_p: 5\nrn: 2.34\nzn: 0.233\nrk: 2.51\nzk: 0.674\na: 0.1\nf: ../data/mcmc_output/mcmc_result.dat\nN_s=20");
            exit(-1);
        }
        cnt++;
    }

    return cl_args;
}


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

/* Load number of bins. Bin edge values are not needed in chain. */
int load_Nbins(void){

    int N;
    char bin_filename[256];
    FILE *bin_file;
    snprintf(bin_filename, 256, "%srbins.ascii.dat", BINS_DIR);
    if((bin_file=fopen(bin_filename,"r"))==NULL){
        fprintf(stderr, "Error: Cannot open file %s \n", bin_filename);
        exit(EXIT_FAILURE);
    }
    fscanf(bin_file, "%d", &N);
    fclose(bin_file);

    return N;
}

/* ----------------------------------------------------------------------- */

/* Load position and density weight data for model stars */
void load_ZRW(POINTING *plist, int lower_ind, int upper_ind, int rank){

    char zrw_filename[256];
    FILE *zrw_file;
    int i, j, N;
    double * Z;
    double * R;
    double * W;

    /* Read star data for each poiting */
    for(i = lower_ind; i < upper_ind; i++){

        snprintf(zrw_filename, 256, "%suniform_ZRW_%s.dat", ZRW_DIR, plist[i].ID);
        if((zrw_file=fopen(zrw_filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s \n", zrw_filename);
            exit(EXIT_FAILURE);
        }
        fscanf(zrw_file, "%d", &N); /* read in number of stars */

        /* Claim arrays */
        Z = calloc(N, sizeof(double));
        R = calloc(N, sizeof(double));
        W = calloc(N, sizeof(double));

        /* Read file for zrw data */
        for(j=0; j<N; j++){
            fscanf(zrw_file, "%lf", &Z[j]);
            fscanf(zrw_file, "%lf", &R[j]);
            fscanf(zrw_file, "%lf", &W[j]);
        }

        fclose(zrw_file);

        /* Assign value to plist element */
        plist[i].N_stars = N;
        plist[i].Z = Z;
        plist[i].R = R;
        plist[i].weight = W;
    }

    if(rank==0) fprintf(stderr, "Model data loaded from %s\n", ZRW_DIR);
}

/* ----------------------------------------------------------------------- */

/* Load data for each bin from a variety of files */
void load_rbins(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank){

    char filename[256];
    FILE *file;
    int i, j;
    RBIN *b;

    /* Loop over each pointing */
    for( i = lower_ind; i<upper_ind; i++ ){

        /* Claim space for bin data */
        b = calloc(N_bins, sizeof(RBIN));

        /* First load DD counts */
        /* Also assign Bin ID */
        snprintf(filename, 256, "%sdd_%s.dat", DD_DIR, plist[i].ID);
        if((file=fopen(filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s\n", filename);
            exit(EXIT_FAILURE);
        }
        for( j=0; j<N_bins; j++ ){
            fscanf(file, "%lf", &b[j].DD);
            snprintf(b[j].binID, 256, "%d", j);
        }
        fclose(file);

        /* Load fractional errors */
        snprintf(filename, 256, "%sfrac_error_%s.dat", ERR_DIR, plist[i].ID);
        if((file=fopen(filename,"r"))==NULL){
            fprintf(stderr, "Error: Cannot open file %s\n", filename);
            exit(EXIT_FAILURE);
        }
        for(j=0; j<N_bins; j++){
            fscanf(file, "%lf", &b[j].frac_error);
        }
        fclose(file);

        /* Assign values to plist elements */
        plist[i].rbin = b;
    }
    if(rank==0){
        fprintf(stderr, "DD counts loaded from %s\n", DD_DIR);
        fprintf(stderr, "Errors loaded from %s\n", ERR_DIR);
    }
}

/* ----------------------------------------------------------------------- */

/* Load pairs for each bin in each l.o.s. */
void load_pairs(POINTING *plist, int N_bins, int lower_ind, int upper_ind, int rank){

    char pair_filename[256];
    FILE *pair_file;
    int i, j;
    unsigned int k, N;
    int *pair1;
    int *pair2;

    /* Loop over each pointing */
    for(i=lower_ind; i<upper_ind; i++){

        for(j=0; j<N_bins; j++){
            snprintf(pair_filename, 256, "%scounts_%s.bin_%s.dat", PAIRS_DIR,
                plist[i].ID, plist[i].rbin[j].binID);
            if((pair_file=fopen(pair_filename,"r"))==NULL){
                fprintf(stderr, "Error: Cannot open file %s\n", pair_filename);
                exit(EXIT_FAILURE);
            }

            /* First get number of pairs */
            fscanf(pair_file, "%u", &N);

            /* Claim arrays */
            pair1 = calloc(N, sizeof(int));
            pair2 = calloc(N, sizeof(int));

            for(k=0; k<N; k++){
                fscanf(pair_file, "%d", &pair1[k]);
                fscanf(pair_file, "%d", &pair2[k]);
            }

            fclose(pair_file);

            /* Assign values to plist elements */
            plist[i].rbin[j].N_pairs = N;
            plist[i].rbin[j].pair1 = pair1;
            plist[i].rbin[j].pair2 = pair2;
        }

    }
    if(rank == 0)fprintf(stderr, "Pairs loaded from %s\n", PAIRS_DIR);
}

/* ----------------------------------------------------------------------- */


/* Output mcmc data to a file */
void output_mcmc(int index, STEP_DATA p, FILE *output_file){

    /* Output column headers as first line */
    if(index==0){
        fprintf( output_file, "step\tchi2\tchi2_red\tr0_thin\tz0_thin\tr0_thick\tz0_thick\tratio\n");
    }

    fprintf( output_file, "%d\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\n",
        index, p.chi2, p.chi2_reduced, p.r0_thin, p.z0_thin,
        p.r0_thick, p.z0_thick, p.ratio_thick_thin );
}

/* ----------------------------------------------------------------------- */
