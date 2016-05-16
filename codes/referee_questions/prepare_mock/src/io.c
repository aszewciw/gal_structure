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

/* get parameters for thin disk */
void get_thin_params( PARAMS *p, unsigned long int N ){

    long double temp;

    p->ratio = 0.1; // should be the same for both disks
    temp = (long double)N * p->ratio;
    p->N_stars = N - (unsigned long int)temp;
    p->z0 = 0.233;
    p->r0 = 2.34;
    p->r_min = 5.0;
    p->r_max = 11.0;
    p->z_min = 0.0;
    p->z_max = 3.0;
    p->phi_max = atan(0.5);
    p->phi_min = -p->phi_max;
    p->phi_min += M_PI;
    p->phi_max += M_PI;
    p->phi_range = p->phi_max - p->phi_min;

    p->r0_pdf_norm = 1.0 / ( p->r0 * ( exp( -p->r_min / p->r0 )
        - exp( -p->r_max / p->r0 ) ) );
    p->z0_pdf_norm = 1.0 / ( 2.0 * p->z0 * ( tanh( p->z_max / (2.0 * p->z0) )
        - tanh( p->z_min / p->z0 ) ) );

    fprintf(stderr, "%lu stars in the thin disk. \n", p->N_stars);

}

/* ----------------------------------------------------------------------- */

/* get parameters for thin disk */
void get_thick_params( PARAMS *p, unsigned long int N ){

    long double temp;

    p->ratio = 0.1; // should be the same for both disks
    temp = (long double)N * p->ratio;
    p->N_stars = (unsigned long int)temp;
    p->z0 = 0.674;
    p->r0 = 2.51;
    p->r_min = 5.0;
    p->r_max = 11.0;
    p->z_min = 0.0;
    p->z_max = 3.0;
    p->phi_max = atan(0.5);
    p->phi_min = -p->phi_max;
    p->phi_min += M_PI;
    p->phi_max += M_PI;
    p->phi_range = p->phi_max - p->phi_min;

    p->r0_pdf_norm = 1.0 / ( p->r0 * ( exp( -p->r_min / p->r0 )
        - exp( -p->r_max / p->r0 ) ) );
    p->z0_pdf_norm = 1.0 / ( 2.0 * p->z0 * ( tanh( p->z_max / (2.0 * p->z0) )
        - tanh( p->z_min / p->z0 ) ) );

    fprintf(stderr, "%lu stars in the thick disk. \n", p->N_stars);

}

// /* ----------------------------------------------------------------------- */
// /* get parameters for thick disk */
// void get_thick_params( PARAMS *p, unsigned long int N ){

//     double temp;

//     p.ratio = 0.1; // should be the same for both disks
//     temp = (double)N * p.ratio;
//     p.N_stars = (int)temp;
//     p.z0 = 0.674;
//     p.r0 = 2.51;
//     p.r_min = 5.0;
//     p.r_max = 11.0;
//     p.z_min = 0.0;
//     p.z_max = 3.0;
//     p.phi_max = atan(0.5);
//     p.phi_min = -phi_max;
//     p.phi_min += M_PI;
//     p.phi_max += M_PI;
//     p.phi_range = phi_max - phi_min;

//     p.r0_pdf_norm = 1.0 / ( p.r0 * ( exp( -p.r_min / p.r0 )
//         - exp( -p.r_max / p.r0 ) ) );
//     p.z0_pdf_norm = 1.0 / ( 2.0 * p.z0 * ( tanh( p.z_max / (2.0 * p.z0) )
//         - tanh( p.z_min / p.z0 ) ) );

//     fprintf(stderr, "%lu stars in the thick disk. \n", p.N_stars);

// }

// /* ----------------------------------------------------------------------- */