#include "config.h"

/*---------------------------------------------------------------------------*/

int main( int argc, char **argv ){

    if (argc != 2){
        fprintf( stderr, "Error. Usage: %s num_stars\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    unsigned long int N_stars;
    sscanf(argv[1], "%lu", &N_stars);

    fprintf(stderr, "Making a galaxy with %lu stars.\n", N_stars);

    unsigned long int N_stars_thin, N_stars_thick, i;
    double r0_thin, z0_thin, r0_thick, z0_thick, thick_thin_ratio;
    double temp;
    double r_min, r_max, z_min, z_max, phi_min, phi_max, phi_range;
    double r0_thin_pdf_norm, z0_thin_pdf_norm;
    double r0_thick_pdf_norm, z0_thick_pdf_norm;
    time_t t;
    int flag; // A flag to make sure points fall within 1-3 kpc
    double Z_temp, R_temp, phi_temp, dist_temp;

    /* Set model parameters */
    /* From Mao et al */
    r0_thin = 2.34;
    z0_thin = 0.233;
    r0_thick = 2.51;
    z0_thick = 0.674;
    thick_thin_ratio = 0.1;

    /* Number of stars in each disk */
    temp = (double)N_stars * thick_thin_ratio;
    N_stars_thick = (int)temp;
    N_stars_thin = N_stars - N_stars_thick;

    /* Set spatial limits for r, z, and phi */
    r_min = 5.0;
    r_max = 11.0;
    z_min = 0.0;
    z_max = 3.0;
    phi_max = atan(0.5);
    phi_min = -phi_max;
    phi_min += M_PI;
    phi_max += M_PI;
    phi_range = phi_max - phi_min;

    /* Normalize PDFs */
    r0_thin_pdf_norm = 1.0 / ( r0_thin * ( exp( -r_min / r0_thin )
        - exp( -r_max / r0_thin ) ) );
    r0_thick_pdf_norm = 1.0 / ( r0_thick * ( exp( -r_min / r0_thick )
        - exp( -r_max / r0_thick ) ) );
    z0_thin_pdf_norm = 1.0 / ( 2.0 * z0_thin * ( tanh( z_max / (2.0 * z0_thin) )
        - tanh( z_min / z0_thin ) ) );
    z0_thick_pdf_norm = 1.0 / ( 2.0 * z0_thick * ( tanh( z_max / (2.0 * z0_thick) )
        - tanh( z_min / z0_thick ) ) );

    /* Allocate arrays for galactic coordinates */
    STAR * thin = malloc(N_stars_thin * sizeof(STAR));
    STAR * thick = malloc(N_stars_thick * sizeof(STAR));

    srand((unsigned) time(&t));

    /* Fill thin disk arrays */
    fprintf(stderr, "Getting Z, R, phi, and distance for thin disk stars. \n");
    /* Make sure we only get stars in the 1-3 kpc range */
    for( i=0; i<N_stars_thin; i++ ){
        flag = 0;
        while(flag==0){
            Z_temp = random_gal_Z(z0_thin, z0_thin_pdf_norm, z_min, z_max);
            R_temp = random_gal_R(r0_thin, r0_thin_pdf_norm, r_min, r_max);
            phi_temp = ( ( (double)rand() / (double)RAND_MAX )
                * phi_range + phi_min );
            dist_temp = get_distance(Z_temp, R_temp, phi_temp);

            /* Break out of while loop if condition is met */
            if( (dist_temp >= 1.0) && (dist_temp <= 3.0) ) flag = 1;
        }

        thin[i].gal_z = Z_temp;
        thin[i].gal_r = R_temp;
        thin[i].gal_phi = phi_temp;
        thin[i].distance = dist_temp;
    }

    /* Fill thick disk arrays */
    fprintf(stderr, "Getting Z, R, phi, and distance for thick disk stars. \n");
    /* Make sure we only get stars in the 1-3 kpc range */
    for( i=0; i<N_stars_thick; i++ ){
        flag = 0;
        while(flag==0){
            Z_temp = random_gal_Z(z0_thick, z0_thick_pdf_norm, z_min, z_max);
            R_temp = random_gal_R(r0_thick, r0_thick_pdf_norm, r_min, r_max);
            phi_temp = ( ( (double)rand() / (double)RAND_MAX )
                * phi_range + phi_min );
            dist_temp = get_distance(Z_temp, R_temp, phi_temp);

            /* Break out of while loop if condition is met */
            if( (dist_temp >= 1.0) && (dist_temp <= 3.0) ) flag = 1;
        }

        thick[i].gal_z = Z_temp;
        thick[i].gal_r = R_temp;
        thick[i].gal_phi = phi_temp;
        thick[i].distance = dist_temp;
    }

    /* Fill thin disk arrays */
    fprintf(stderr, "Getting remaining coordinates for thin disk stars. \n");
    #pragma simd
    for( i=0; i<N_stars_thin; i++ ){
        ZR_to_gal(&thin[i]);
        gal_to_eq(&thin[i]);
        eq_to_cart(&thin[i]);
    }

    /* Fill thick disk arrays */
    fprintf(stderr, "Getting remaining coordinates for thick disk stars. \n");
    #pragma simd
    for( i=0; i<N_stars_thick; i++ ){
        ZR_to_gal(&thick[i]);
        gal_to_eq(&thick[i]);
        eq_to_cart(&thick[i]);
    }

    char output_filename[256];
    FILE *output_file;

    /* Write thin disk */
    snprintf(output_filename, 256, "%smocktest_thin.dat", OUT_DIR);
    fprintf(stderr, "Writing thin stars to %s\n", output_filename);
    output_file = fopen(output_filename, "a");
    /* first write number of stars */
    fprintf(output_file, "%lu\n", N_stars_thin);
    for( i=0; i<N_stars_thin; i++ ){
        fprintf(output_file,
            "%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\n",
            thin[i].gal_z, thin[i].gal_r, thin[i].gal_phi,
            thin[i].gal_l_rad, thin[i].gal_b_rad,
            thin[i].ra_rad, thin[i].dec_rad, thin[i].distance,
            thin[i].x, thin[i].y, thin[i].z);
    }
    fclose(output_file);

    /* Write thick disk */
    snprintf(output_filename, 256, "%smocktest_thick.dat", OUT_DIR);
    fprintf(stderr, "Writing thick stars to %s\n", output_filename);
    output_file = fopen(output_filename, "a");
    fprintf(output_file, "%lu\n", N_stars_thick);
    for( i=0; i<N_stars_thick; i++ ){
        fprintf(output_file,
            "%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\n",
            thick[i].gal_z, thick[i].gal_r, thick[i].gal_phi,
            thick[i].gal_l_rad, thick[i].gal_b_rad,
            thick[i].ra_rad, thick[i].dec_rad, thick[i].distance,
            thick[i].x, thick[i].y, thick[i].z);
    }
    fclose(output_file);


    /* Deallocate arrays */
    free(thin);
    free(thick);
    fprintf(stderr, "Files Written. Arrays deallocated.\n");


    return 0;
}