#include "config.h"

/* ----------------------------------------------------------------------- */

/* Load info for different SEGUE plate sky positions */
void load_pointing_list(int *N_plist, POINTING **plist){

    char plist_filename[256];
    snprintf(plist_filename, 256, "%stodo_list.ascii.dat", DATA_DIR);

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

void get_params( PARAMS *p, unsigned long int N ){

    /*
    Get parameters according to the canonical two-disk model
    of those two guys who made a two-disk model...shit, what
    are their names?

    Regardless, can check Mao et al., 2015, for the functional
    form that is used throughout this project.
    */

    /* Disk params */
    p->z0_thin  = 0.233;
    p->r0_thin  = 2.34;
    p->z0_thick = 0.674;
    p->r0_thick = 2.51;
    // p->ratio    = 0.1;
    p->ratio = 0.0;

    /* Geometric sample limits */
    /* These are slightly generous limits. Sample is cut down
    appropriately elsewhere */
    p->r_min     = 4.5;
    p->r_max     = 11.5;
    p->z_min     = 0.0;
    p->z_max     = 3.1;
    p->phi_max   = atan(0.5);
    p->phi_min   = -p->phi_max;
    p->phi_min   += M_PI;
    p->phi_max   += M_PI;
    p->phi_range = p->phi_max - p->phi_min;

    /* PDF normalizations */
    /* thin normalizations */
    p->r0_pdf_norm_thin = 1.0 / ( p->r0_thin
        * ( exp( -p->r_min / p->r0_thin )
        - exp( -p->r_max / p->r0_thin ) ) );
    p->z0_pdf_norm_thin = 1.0 / ( 2.0 * p->z0_thin
        * ( tanh( p->z_max / (2.0 * p->z0_thin) )
        - tanh( p->z_min / (2.0 * p->z0_thin) ) ) );
    /*thick normalizations */
    p->r0_pdf_norm_thick = 1.0 / ( p->r0_thick
        * ( exp( -p->r_min / p->r0_thick )
        - exp( -p->r_max / p->r0_thick ) ) );
    p->z0_pdf_norm_thick = 1.0 / ( 2.0 * p->z0_thick
        * ( tanh( p->z_max / (2.0 * p->z0_thick) )
        - tanh( p->z_min / (2.0 * p->z0_thick) ) ) );

    /* Get number of stars in each disk */
    /* This could be done as a separate function */
    /*
    It is difficult to detail the logic of these steps.
    What I am doing is integrating the density over the
    volume and setting this equal to the total number of
    stars to find the density normalization constant. I
    then use this normalization to find the stars in each
    disk.
    */
    double Z_integrated; /* integral of sech^2(Z) term */
    double R_integrated; /* integral of exp(-R) term */
    double thin_term; /* combined integral term for thin disk */
    double thick_term; /* combined integral term for thick disk */
    long double density_const; /* normalization of density */

    Z_integrated = 2.0 * p->z0_thin * (
        tanh( p->z_max / (2.0*p->z0_thin) )
        - tanh( p->z_min / (2.0*p->z0_thin) ) );
    R_integrated = -p->r0_thin * (
        exp(-p->r_max/p->r0_thin) * (p->r0_thin + p->r_max)
        - exp(-p->r_min/p->r0_thin) * (p->r0_thin + p->r_min) );
    thin_term = Z_integrated * R_integrated * p->phi_range; //phi range doesn't actually matter but is put in for completeness

    Z_integrated = 2.0 * p->z0_thick * (
        tanh( p->z_max / (2.0*p->z0_thick) )
        - tanh( p->z_min / (2.0*p->z0_thick) ) );
    R_integrated = -p->r0_thick * (
        exp(-p->r_max/p->r0_thick) * (p->r0_thick + p->r_max)
        - exp(-p->r_min/p->r0_thick) * (p->r0_thick + p->r_min) );
    thick_term = p->ratio * Z_integrated * R_integrated * p->phi_range;

    density_const = (long double)N / (thin_term + thick_term);

    long double temp = density_const * thin_term;

    p->N_thin = (unsigned long int)temp;

    temp = density_const * thick_term;

    p->N_thick = (unsigned long int)temp + 1;

    fprintf(stderr, "%lu stars in the thin disk. \n", p->N_thin);
    fprintf(stderr, "%lu stars in the thick disk. \n", p->N_thick);
    fprintf(stderr, "%lu total stars. \n", p->N_thin + p->N_thick);


}

/* ----------------------------------------------------------------------- */

/* output stars' cartesian coordinates to a file */
void output_data( FILE *output_file, double density_analytic,
    double density_mock, DVOL dv)
{
    fprintf( output_file, "%lf\t%lf\t%lf\n",
        density_analytic, density_mock, dv.volume);
}

/* ----------------------------------------------------------------------- */
