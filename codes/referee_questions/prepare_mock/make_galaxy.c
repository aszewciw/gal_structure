#include "config.h"

/*---------------------------------------------------------------------------*/

/* Return a galactic height */
double random_gal_Z(double z0, double pdf_norm, double z_min, double z_max)
{
    double cdf, b, temp, z, plus_minus;

    cdf = (double)rand() / (double)RAND_MAX;
    b = tanh( z_min / (2.0 * z0) );
    temp = ( cdf / (pdf_norm * 2.0 * z0) ) + b;
    z = atanh(temp) * 2.0 * z0;

    /* Generate + or - 1.0 */
    plus_minus = floor( 2.0 * (double)rand() / (double)RAND_MAX );
    plus_minus = plus_minus * 2.0 - 1.0;

    z *= plus_minus;
    return z;
}

/*---------------------------------------------------------------------------*/

/* Return distance in galactic plane */
double random_gal_R(double r0, double pdf_norm, double r_min, double r_max)
{
    double cdf, b, exp_term, r;

    cdf = (double)rand() / (double)RAND_MAX;
    b = exp(-r_min / r0);
    exp_term = b - ( cdf / (pdf_norm * r0) );
    r = -r0 * log(exp_term);

    return r;
}

/*---------------------------------------------------------------------------*/
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
    // double * z_thin_gal = malloc(N_stars_thin * sizeof(double));
    // double * r_thin_gal = malloc(N_stars_thin * sizeof(double));
    // double * phi_thin_gal = malloc(N_stars_thin * sizeof(double));
    // double * x_thin_gal = malloc(N_stars_thin * sizeof(double));
    // double * y_thin_gal = malloc(N_stars_thin * sizeof(double));
    // double * z_thick_gal = malloc(N_stars_thick * sizeof(double));
    // double * r_thick_gal = malloc(N_stars_thick * sizeof(double));
    // double * phi_thick_gal = malloc(N_stars_thick * sizeof(double));
    // double * x_thick_gal = malloc(N_stars_thick * sizeof(double));
    // double * y_thick_gal = malloc(N_stars_thick * sizeof(double));
    STAR * thin = malloc(N_stars_thin * sizeof(STAR));
    STAR * thick = malloc(N_stars_thick * sizeof(STAR));

    srand((unsigned) time(&t));

    // char output_filename[256];
    // FILE *output_file;
    // snprintf(output_filename, 256, "%smocktest_thin.dat", OUT_DIR);
    // output_file = fopen(output_filename, "a");

    /* Fill thin disk arrays */
    for( i=0; i<N_stars_thin; i++ ){
        // z_thin_gal[i] = random_z(z0_thin, z0_thin_pdf_norm, z_min, z_max);
        // r_thin_gal[i] = random_r(r0_thin, r0_thin_pdf_norm, r_min, r_max);
        // phi_thin_gal[i] = ( ((double)rand() / (double)RAND_MAX) * phi_range
        //     + phi_min );
        // x_thin_gal[i] = r_thin_gal[i] * cos(phi_thin_gal[i]);
        // y_thin_gal[i] = r_thin_gal[i] * sin(phi_thin_gal[i]);
        thin[i].gal_z = random_gal_Z(z0_thin, z0_thin_pdf_norm, z_min, z_max);
        thin[i].gal_r = random_gal_R(r0_thin, r0_thin_pdf_norm, r_min, r_max);
        thin[i].gal_phi = ( ( (double)rand() / (double)RAND_MAX )
            * phi_range + phi_min );
        ZR_to_gal(&thin[i]);
        gal_to_eq(&thin[i]);
        eq_to_cart(&thin[i]);


        // fprintf(output_file, "%lf\t%lf\t%lf\t%lf\n", x_thin_gal[i], y_thin_gal[i],
        //     z_thin_gal[i], r_thin_gal[i]);
    }

    // fclose(output_file);

    // snprintf(output_filename, 256, "%smocktest_thick.dat", OUT_DIR);
    // output_file = fopen(output_filename, "a");

    /* Fill thick disk arrays */
    for( i=0; i<N_stars_thick; i++ ){
        // z_thick_gal[i] = random_z(z0_thick, z0_thick_pdf_norm, z_min, z_max);
        // r_thick_gal[i] = random_r(r0_thick, r0_thick_pdf_norm, r_min, r_max);
        // phi_thick_gal[i] = ( ((double)rand() / (double)RAND_MAX) * phi_range
        //     + phi_min );
        // x_thick_gal[i] = r_thick_gal[i] * cos(phi_thick_gal[i]);
        // y_thick_gal[i] = r_thick_gal[i] * sin(phi_thick_gal[i]);

        // fprintf(output_file, "%lf\t%lf\t%lf\t%lf\n", x_thick_gal[i], y_thick_gal[i],
        //     z_thick_gal[i], r_thick_gal[i]);
        thick[i].gal_z = random_gal_Z(z0_thick, z0_thick_pdf_norm, z_min, z_max);
        thick[i].gal_r = random_gal_R(r0_thick, r0_thick_pdf_norm, r_min, r_max);
        thick[i].gal_phi = ( ( (double)rand() / (double)RAND_MAX )
            * phi_range + phi_min );
        ZR_to_gal(&thick[i]);
        gal_to_eq(&thick[i]);
        eq_to_cart(&thick[i]);
    }

    // fclose(output_file);

    /* Deallocate arrays */
    // free(z_thin_gal);
    // free(r_thin_gal);
    // free(phi_thin_gal);
    // free(x_thin_gal);
    // free(y_thin_gal);
    // free(z_thick_gal);
    // free(r_thick_gal);
    // free(phi_thick_gal);
    // free(x_thick_gal);
    // free(y_thick_gal);
    free(thin);
    free(thick);


    return 0;
}