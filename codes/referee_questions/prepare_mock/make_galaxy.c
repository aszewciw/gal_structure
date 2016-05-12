#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>
#include <math.h>
#include <time.h>
#include <string.h>

/* Directories */
#define OUT_DIR "./out_data/"

/* J2000 Coordinates in radians, kpc */
#define GALACTIC_CENT_RA 4.6496461
#define GALACTIC_CENT_DEC -0.50503153
#define GALACTIC_CENT_DIST 8.33
#define GALACTIC_NP_RA 3.36603341
#define GALACTIC_NP_DEC 0.47347878
#define GALACTIC_ASC_NODE 0.57477
#define GALACTIC_SUN_R 8.0
#define GALACTIC_SUN_Z 0.02

/* A holder for a vector in Cartesian coordinates */
typedef struct VECTOR{
    double x, y, z;
} VECTOR;

typedef struct STAR{
    double ra_rad, dec_rad, distance;
    double galactic_l_rad, galactic_b_rad;
    double galactic_Z, galactic_R;
    double x, y, z;
} STAR;
/*---------------------------------------------------------------------------*/

/* Return a galactic height */
double random_z(double z0, double pdf_norm, double z_min, double z_max)
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
double random_r(double r0, double pdf_norm, double r_min, double r_max)
{
    double cdf, b, exp_term, r;

    cdf = (double)rand() / (double)RAND_MAX;
    b = exp(-r_min / r0);
    exp_term = b - ( cdf / (pdf_norm * r0) );
    r = -r0 * log(exp_term);

    return r;
}

/*---------------------------------------------------------------------------*/

/* Galactic North Pole in J2000, in degrees! */
const double Galactic_North_Pole_RA = 192.859508;
const double Galactic_North_Pole_Dec = 27.128336;
const double Galactic_Ascending_Node = 32.932;
/* Default Sun's position */
const double Sun_R = 8.0;
const double Sun_Z = 0.02;

/*---------------------------------------------------------------------------*/

/* update star's (x, y, z) using (ra, dec, distance)  */
void eq2cart(STAR *s){
    s->x = s->distance * cos(s->ra_rad) * cos(s->dec_rad);
    s->y = s->distance * sin(s->ra_rad) * cos(s->dec_rad);
    s->z = s->distance * sin(s->dec_rad);
}

/*---------------------------------------------------------------------------*/

/* update star's (ra, dec, distance) using (x, y, z) */
void cart2eq(STAR *s){
    s->distance = sqrt(s->x * s->x + s->y * s->y + s->z * s->z);
    s->ra_rad = atan2(s->y, s->x);
    if(s->ra_rad < 0){
        s->ra_rad = 2.0 * PI + s->ra_rad;
    }
    s->dec_rad = asin(s->z / s->distance);
}

/*---------------------------------------------------------------------------*/

/* update star's Galactic (l, b) using (ra, dec)  */
void eq2gal(STAR *s){
    double alpha, delta, la;
    /* convert params to radians */
    alpha = Galactic_North_Pole_RA * PI / 180.0;
    delta = Galactic_North_Pole_Dec * PI / 180.0;
    la = Galactic_Ascending_Node * PI / 180.0;

    double ra, dec, l, b;     /* temporary holders*/
    ra = s->ra_rad;
    dec = s->dec_rad;

    b = asin(sin(dec) * sin(delta) +
       cos(dec) * cos(delta) * cos(ra - alpha));

    l = atan2(sin(dec) * cos(delta) - cos(dec) * sin(delta) * cos(ra - alpha),
        cos(dec) * sin(ra - alpha)
        ) + la;


    if(l < 0) l += 2.0 * PI;

    l = fmod(l, (2.0 * PI));

    s->galactic_l_rad = l;
    s->galactic_b_rad = b;

}

/*---------------------------------------------------------------------------*/

/* update star's (ra, dec) using Galactic (l, b) */
void gal2eq(STAR *s){
    double alpha, delta, la;
    /* convert params to radians */
    alpha = Galactic_North_Pole_RA * PI / 180.0;
    delta = Galactic_North_Pole_Dec * PI / 180.0;
    la = Galactic_Ascending_Node * PI / 180.0;

    double ra, dec, l, b;     /* temporary holders*/
    l = s->galactic_l_rad;
    b = s->galactic_b_rad;

    dec = asin(sin(b) * sin(delta) +
         cos(b) * cos(delta) * sin(l - la));

    ra = atan2(cos(b) * cos(l - la),
         sin(b) * cos(delta) - cos(b) * sin(delta) * sin(l - la)
         ) + alpha;

    if(ra < 0) ra += 2.0 * PI;

    ra = fmod(ra, (2.0 * PI));

    s->ra_rad = ra;
    s->dec_rad = dec;

}

/*---------------------------------------------------------------------------*/

/* update Galactic (Z, R) */
/* This may depend on Sun's position! */
void gal2ZR(STAR *s, PARAMETERS params){

    double sr, sz;
    if(params.sun_position == 1){
        sr = params.sun_R;
        sz = params.sun_Z;
    }
    else{
        sr = Sun_R;
        sz = Sun_Z;
    }

  s->galactic_Z = fabs(s->distance * sin(s->galactic_b_rad) + sz);
  double x, y;
  x = s->distance * cos(s->galactic_b_rad);
  y = sr;
  s->galactic_R = x * x + y * y - 2.0 * x * y * cos(s->galactic_l_rad);

}

/*---------------------------------------------------------------------------*/

/* Dot product of 2 vectors in 3D cartesian space. */
double dot(VECTOR vec1, VECTOR vec2){
    double dp;
    dp = vec1.x * vec2.x + vec1.y * vec2.y + vec1.z * vec2.z;
    return dp;
}

/*---------------------------------------------------------------------------*/

/* Cross product of 2 vectors in 3D Cartesian space. */
VECTOR cross(VECTOR vec1, VECTOR vec2){

    VECTOR result;
    result.x = vec1.y * vec2.z - vec1.z * vec2.y;
    result.y = vec1.z * vec2.x - vec1.x * vec2.z;
    result.z = vec1.x * vec2.y - vec1.y * vec2.x;

    return result;

}

/*---------------------------------------------------------------------------*/

/* This function rotate a vector around an axis in 3D Cartesian space
   using Rodrigues' rotation formula.
*/
VECTOR rodrigues(VECTOR axis, VECTOR vec, double theta_rad){

    /* normalize the axis vector */
    double ar = sqrt(axis.x * axis.x + axis.y * axis.y + axis.z * axis.z);
    axis.x = axis.x / ar;
    axis.y = axis.y / ar;
    axis.z = axis.z / ar;

    /* cross product and dot product */
    VECTOR cp = cross(axis, vec);
    double dp = dot(axis, vec);

    VECTOR result;
    result.x = (vec.x * cos(theta_rad) + cp.x * sin(theta_rad)
          + axis.x * dp * (1 - cos(theta_rad)));

    result.y = (vec.y * cos(theta_rad) + cp.y * sin(theta_rad)
          + axis.y * dp * (1 - cos(theta_rad)));

    result.z = (vec.z * cos(theta_rad) + cp.z * sin(theta_rad)
          + axis.z * dp * (1 - cos(theta_rad)));

    return result;

}


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
    double * z_thin_gal = malloc(N_stars_thin * sizeof(double));
    double * r_thin_gal = malloc(N_stars_thin * sizeof(double));
    double * phi_thin_gal = malloc(N_stars_thin * sizeof(double));
    double * x_thin_gal = malloc(N_stars_thin * sizeof(double));
    double * y_thin_gal = malloc(N_stars_thin * sizeof(double));
    double * z_thick_gal = malloc(N_stars_thick * sizeof(double));
    double * r_thick_gal = malloc(N_stars_thick * sizeof(double));
    double * phi_thick_gal = malloc(N_stars_thick * sizeof(double));
    double * x_thick_gal = malloc(N_stars_thick * sizeof(double));
    double * y_thick_gal = malloc(N_stars_thick * sizeof(double));


    srand((unsigned) time(&t));

    char output_filename[256];
    FILE *output_file;
    snprintf(output_filename, 256, "%smocktest_thin.dat", OUT_DIR);
    output_file = fopen(output_filename, "a");

    /* Fill thin disk arrays */
    for( i=0; i<N_stars_thin; i++ ){
        z_thin_gal[i] = random_z(z0_thin, z0_thin_pdf_norm, z_min, z_max);
        r_thin_gal[i] = random_r(r0_thin, r0_thin_pdf_norm, r_min, r_max);
        phi_thin_gal[i] = ( ((double)rand() / (double)RAND_MAX) * phi_range
            + phi_min );
        x_thin_gal[i] = r_thin_gal[i] * cos(phi_thin_gal[i]);
        y_thin_gal[i] = r_thin_gal[i] * sin(phi_thin_gal[i]);

        fprintf(output_file, "%lf\t%lf\t%lf\t%lf\n", x_thin_gal[i], y_thin_gal[i],
            z_thin_gal[i], r_thin_gal[i]);
    }

    fclose(output_file);

    snprintf(output_filename, 256, "%smocktest_thick.dat", OUT_DIR);
    output_file = fopen(output_filename, "a");

    /* Fill thick disk arrays */
    for( i=0; i<N_stars_thick; i++ ){
        z_thick_gal[i] = random_z(z0_thick, z0_thick_pdf_norm, z_min, z_max);
        r_thick_gal[i] = random_r(r0_thick, r0_thick_pdf_norm, r_min, r_max);
        phi_thick_gal[i] = ( ((double)rand() / (double)RAND_MAX) * phi_range
            + phi_min );
        x_thick_gal[i] = r_thick_gal[i] * cos(phi_thick_gal[i]);
        y_thick_gal[i] = r_thick_gal[i] * sin(phi_thick_gal[i]);

        fprintf(output_file, "%lf\t%lf\t%lf\t%lf\n", x_thick_gal[i], y_thick_gal[i],
            z_thick_gal[i], r_thick_gal[i]);
    }

    fclose(output_file);

    /* Deallocate arrays */
    free(z_thin_gal);
    free(r_thin_gal);
    free(phi_thin_gal);
    free(x_thin_gal);
    free(y_thin_gal);
    free(z_thick_gal);
    free(r_thick_gal);
    free(phi_thick_gal);
    free(x_thick_gal);
    free(y_thick_gal);


    return 0;
}