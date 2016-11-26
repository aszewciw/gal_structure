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
    if(N!=152){
        fprintf(stderr, "Error reading in pointing list\n");
        exit(EXIT_FAILURE);
    }

    /* Claim an array for a list of pointing */
    p = calloc(N, sizeof(POINTING));

    int i;
    for(i = 0; i < N; i++){
        fscanf(plist_file, "%s", p[i].ID);
        fscanf(plist_file, "%lf", &p[i].ra_deg);
        fscanf(plist_file, "%lf", &p[i].dec_deg);
        fscanf(plist_file, "%lf", &p[i].ra_rad);
        fscanf(plist_file, "%lf", &p[i].dec_rad);
        fscanf(plist_file, "%lf", &p[i].galactic_l_rad);
        fscanf(plist_file, "%lf", &p[i].galactic_b_rad);
        fscanf(plist_file, "%lf", &p[i].x);
        fscanf(plist_file, "%lf", &p[i].y);
        fscanf(plist_file, "%lf", &p[i].z);
        fscanf(plist_file, "%d", &p[i].N_data);
        p[i].N_mock = 0;
        p[i].flag = 0;
    }

    fclose(plist_file);

    /* Assign the value to main function arguments */
    *N_plist = N;
    *plist = p;

    fprintf(stderr, "%d pointings to do.\n", N);
}

/* ----------------------------------------------------------------------- */

/* Perform integral over bounds in galactic Z */
/* integral of sech^2(z/2z0)*dz */
double integrate_Z(double z0, double z_min, double z_max){

    double integral;

    integral = ( 2.0 * z0 * ( tanh( z_max / (2.0 * z0) )
        - tanh( z_min / (2.0 * z0) ) ) );

    return integral;
}

/* ----------------------------------------------------------------------- */

/* Perform integral over bounds in galactic R */
/* integral of r*exp(-r/r0)*dr */
double integrate_R(double r0, double r_min, double r_max){

    double integral;

    integral = ( -r0 * ( exp(-r_max/r0)*(r_max + r0)
        - exp(-r_min/r0)*(r_min + r0) ) );

    return integral;
}

/* ----------------------------------------------------------------------- */
/*
Get parameters according to the canonical two-disk model
of those two guys who made a two-disk model...shit, what
are their names?

Regardless, can check Mao et al., 2015, for the functional
form that is used throughout this project.
*/
void get_params( PARAMS *p, unsigned long int N ){

    /* Integral of thick and thin density functions */
    double z_thin_integral;
    double r_thin_integral;
    double z_thick_integral;
    double r_thick_integral;

    /* combined integral terms */
    double thin_term;
    double thick_term;

    /* normalization of density */
    double density_const;

    /* Disk params */
    p->z0_thin  = 0.193;
    p->r0_thin  = 2.34;
    p->z0_thick = 0.674;
    p->r0_thick = 2.51;
    p->ratio    = 0.1;

    /* Generous sized geometric sample limits */
    /* Use to make stars only roughly in solar neighbordhood */
    p->r_min     = 4.5;
    p->r_max     = 11.5;
    p->z_min     = 0.0;
    p->z_max     = 3.1;
    p->phi_max   = atan(0.5);
    p->phi_min   = -p->phi_max;
    p->phi_min   += M_PI;
    p->phi_max   += M_PI;
    p->phi_range = p->phi_max - p->phi_min;

    /* Partial integrals */
    z_thin_integral  = integrate_Z(p->z0_thin, p->z_min, p->z_max);
    r_thin_integral  = integrate_R(p->r0_thin, p->r_min, p->r_max);
    z_thick_integral = integrate_Z(p->z0_thick, p->z_min, p->z_max);
    r_thick_integral = integrate_R(p->r0_thick, p->r_min, p->r_max);

    /* PDF normalizations */
    p->z0_pdf_norm_thin  = 1.0 / z_thin_integral;
    p->r0_pdf_norm_thin  = 1.0 / r_thin_integral;
    p->z0_pdf_norm_thick = 1.0 / z_thick_integral;
    p->r0_pdf_norm_thick = 1.0 / r_thick_integral;


    /* Get number of stars in each disk */
    /* extra factor of 2 accounts for symmetry about MW plane */
    /* thin and thick integrals */
    thin_term  = 2.0 * z_thin_integral * r_thin_integral * p->phi_range;
    thick_term = 2.0 * p->ratio * z_thick_integral * r_thick_integral * p->phi_range;

    /* normalize to get density constant */
    density_const = (double)N / (thin_term + thick_term);

    /* get stars in thin disk */
    long double temp = density_const * thin_term;
    p->N_thin = (unsigned long int)temp;

    /* get stars in thick disk */
    /* add 1 to account for int roundoff */
    temp = density_const * thick_term;
    p->N_thick = (unsigned long int)temp + 1;

    fprintf(stderr, "%lu stars in the thin disk. \n", p->N_thin);
    fprintf(stderr, "%lu stars in the thick disk. \n", p->N_thick);
    fprintf(stderr, "%lu total stars. \n", p->N_thin + p->N_thick);
}

/* ----------------------------------------------------------------------- */

/* output stars' cartesian coordinates to a file */
void output_star( FILE *output_file, STAR s){
    fprintf( output_file, "%lf\t%lf\t%lf\n", s.x, s.y, s.z );
}

/* ----------------------------------------------------------------------- */
