#include "config.h"

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

/* dot product of two unit vectors */
double dot_product(VECTOR v1, VECTOR v2){
    double dot;

    dot = v1.x * v2.x + v1.y * v2.y + v1.z * v2.z;

    return dot;
}

/*---------------------------------------------------------------------------*/

void generate_stars( STAR *s, PARAMS *p ){

    int flag;
    unsigned long int i;
    double Z_temp, R_temp, phi_temp, dist_temp;

    /* Make sure we only get stars in the 1-3 kpc range */
    for( i=0; i<p->N_stars; i++ ){
        flag = 0;
        while(flag==0){
            Z_temp = random_gal_Z(p->z0, p->z0_pdf_norm, p->z_min, p->z_max);
            R_temp = random_gal_R(p->r0, p->r0_pdf_norm, p->r_min, p->r_max);
            phi_temp = ( ( (double)rand() / (double)RAND_MAX )
                * p->phi_range + p->phi_min );
            dist_temp = get_distance(Z_temp, R_temp, phi_temp);

            /* Break out of while loop if condition is met */
            if( (dist_temp >= 1.0) && (dist_temp <= 3.0) ) flag = 1;
        }

        s[i].gal_z = Z_temp;
        s[i].gal_r = R_temp;
        s[i].gal_phi = phi_temp;
        s[i].distance = dist_temp;
    }

    fprintf(stderr, "Getting remaining coordinates. \n");
    #pragma simd
    for( i=0; i<p.N_stars; i++ ){
        ZR_to_gal(&s[i]);
        gal_to_eq(&s[i]);
        eq_to_cart(&s[i]);
    }
}

/*---------------------------------------------------------------------------*/

void separate_sample(POINTING *p, STAR *s, int N_p, unsigned long int N_s){

    int i;
    unsigned long int j;
    char filename[256];
    FILE *file;
    VECTOR plate, point;
    double dot_prod;
    double plate_cos;
    int star_count;

    plate_cos = cos( PLATE_RADIUS_DEG * M_PI / 180. );

    for(i=0; i<N_p; i++){

        if( p[i].flag == 1) continue;
        snprintf(filename, 256, "%smock_%s.xyz.dat", DATA_DIR, p[i].ID);
        file = fopen(filename, "a");
        star_count = 0;

        /* plate unit vector */
        plate.x = p[i].x;
        plate.y = p[i].y;
        plate.z = p[i].z;

        for(j=0; j<N_s; j++){

            /* unit vectors */
            point.x = s[j].x / s[j].distance;
            point.y = s[j].y / s[j].distance;
            point.z = s[j].z / s[j].distance;

            dot_prod = dot_product(plate, point);

            if(dot_prod >= plate_cos){
                star_count += 1;
                fprintf( file, "%lf\t%lf\t%lf\n", s[j].x, s[j].y, s[j].z );
            }
        }
        p[i].N_mock += star_count;
        fclose(file);
    }
}

/*---------------------------------------------------------------------------*/
