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

double normalize_PDF_Z(double z0, double z_min, double z_max){

    double pdf_norm;

    pdf_norm = 1.0 / ( log(z_max+z0) - log(z_min+z0) );

    return pdf_norm;
}

/* ----------------------------------------------------------------------- */

double normalize_PDF_R(double r0, double r_min, double r_max){

    double pdf_norm, max_term, min_term;

    max_term = 0.5*r_max*r_max + r0*r_max;
    min_term = 0.5*r_min*r_min + r0*r_min;

    pdf_norm = 1.0 / ( max_term - min_term );

    return pdf_norm;
}

/* ----------------------------------------------------------------------- */

void get_params( PARAMS *p, unsigned long int N ){

    p->z1    = 0.2;
    p->r1    = 1.0;
    p->z2    = 0.3;
    p->r2    = 2.0;
    p->ratio = 0.2;

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
    p->z1_pdf_norm = normalize_PDF_Z(p->z1, p->z_min, p->z_max);
    p->r1_pdf_norm = normalize_PDF_R(p->r1, p->r_min, p->r_max);
    p->z2_pdf_norm = normalize_PDF_Z(p->z2, p->z_min, p->z_max);
    p->r2_pdf_norm = normalize_PDF_R(p->r2, p->r_min, p->r_max);


    double Z_integrated;        /* integral of sech^2(Z) term */
    double R_integrated;        /* integral of exp(-R) term */
    double pop1_term;           /* combined integral term for thin disk */
    double pop2_term;           /* combined integral term for thick disk */
    long double density_const;  /* normalization of density */

    /* NOTE: technically I should be multiplying the z terms
    by another factor of 2 to account for stars both above
    and below the disk, but it cancels out when I get N_pop1
    and N_pop2 */

    Z_integrated = 2.0 / p->z1_pdf_norm;
    R_integrated = 1.0 / p->r1_pdf_norm;
    pop1_term = Z_integrated * R_integrated * p->phi_range;

    Z_integrated = 2.0 / p->z2_pdf_norm;
    R_integrated = 1.0 / p->r2_pdf_norm;
    pop2_term = p->ratio * Z_integrated * R_integrated * p->phi_range;

    density_const = (long double)N / (pop1_term + pop2_term);

    long double temp = density_const * pop1_term;

    p->N_pop1 = (unsigned long int)temp;

    temp = density_const * pop2_term;

    p->N_pop2 = (unsigned long int)temp + 1;

    fprintf(stderr, "%lu stars in pop 1. \n", p->N_pop1);
    fprintf(stderr, "%lu stars in pop 2. \n", p->N_pop2);
    fprintf(stderr, "%lu total stars. \n", p->N_pop1 + p->N_pop2);


}

/* ----------------------------------------------------------------------- */

/* output stars' cartesian coordinates to a file */
void output_star( FILE *output_file, STAR s){
    fprintf( output_file, "%lf\t%lf\t%lf\n", s.x, s.y, s.z );
}

/* ----------------------------------------------------------------------- */
