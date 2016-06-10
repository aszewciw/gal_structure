#include "config.h"

/* Return a galactic height according to distribution */
double random_gal_Z(double z0, double pdf_norm, double z_min){

    /* invert the cdf to draw randomly from distribution */
    double cdf;         // Cumulative distribution function
    double b;           // lower bound (see below)
    double temp;        // temporary term
    double z;           // magnitude of height
    double plus_minus;  // random assignment above or below gal plane

    /* get a random z */
    cdf  = (double)rand() / (double)RAND_MAX;
    b    = tanh( z_min / (2.0 * z0) );
    temp = ( cdf / (pdf_norm * 2.0 * z0) ) + b;
    z    = atanh(temp) * 2.0 * z0;

    /* Generate + or - 1.0 */
    plus_minus = floor( 2.0 * (double)rand() / (double)RAND_MAX );
    plus_minus = plus_minus * 2.0 - 1.0;

    z *= plus_minus;
    return z;
}

/*---------------------------------------------------------------------------*/

/* Return a galactic in-plane radius according to distribution */
double random_gal_R(double r0, double pdf_norm, double r_min){

    /* the cdf to draw from the distribution */
    double cdf;         // Cumulative distribution function
    double min_term;    // lower bound (see below)

    /* temporary constants in solving equation */
    double const1, const2, const3;

    /* terms used in bisection root finder */
    int i, max_steps;   // steps in root finder
    double a, b, c;     // endpoints and midpoint
    double f_b, f_c;    // f(b) and f(c)
    double tol;         // threshhold for accepting root

    /* alternate method */
    cdf      = (double)rand() / (double)RAND_MAX;
    const1   = cdf/pdf_norm;
    const2   = const1 / -r0;
    min_term = exp(-r_min/r0)*(r_min+r0);
    const3   = min_term + const2;

    /* set limits and initialize values for bisection */
    i = 0;
    max_steps = 100;
    tol = 0.00001;
    f_c = 1.0;
    a = r_min;
    b = r_max;

    /* Get dat rooty! */
    while(fabs(f_c)>tol && i<max_steps){
        i+=1;
        c = (a+b)/2.0;

        f_c = exp(-c/r0)*(c+r0) - const3;
        f_b = exp(-b/r0)*(b+r0) - const3;

        if((f_c * f_b)>0) b = c;
        else a = c;
    }

    /* check if we didn't manage to converge in less than 100 steps */
    if(i==max_steps) fprintf(stderr, "Oh no! Took more than 100 steps to converge!\n");
    return c;
}

/*---------------------------------------------------------------------------*/

/* dot product of two unit vectors */
double dot_product(VECTOR v1, VECTOR v2){

    double dot;

    dot = v1.x * v2.x + v1.y * v2.y + v1.z * v2.z;

    return dot;
}

/*---------------------------------------------------------------------------*/

/* make a temporary number of stars */
void generate_stars( STAR *s, PARAMS *p, int disk_type ){

    int flag;                   // check if star is within distance limits
    double Z_temp;              // temp galactic height
    double R_temp;              // temp galactic in-plane distance
    double phi_temp;            // temp galactic angle
    double dist_temp;           // temporary sun-star distance
    double z0;                  // disk scale height
    double r0;                  // disk scale length
    double z0_pdf_norm;         // PDF height normalization
    double r0_pdf_norm;         // PDF length normalization
    unsigned long int i;        // loop variable...obvi
    unsigned long int N_stars;  // number of stars in disk

    /* parse disk_type to decide if thin or thick */
    if(disk_type==0){
        /* use thin disk */
        N_stars     = p->N_thin;
        z0          = p->z0_thin;
        r0          = p->r0_thin;
        z0_pdf_norm = p->z0_pdf_norm_thin;
        r0_pdf_norm = p->r0_pdf_norm_thin;
    }
    else if(disk_type==1){
        /* use thick disk */
        N_stars     = p->N_thick;
        z0          = p->z0_thick;
        r0          = p->r0_thick;
        z0_pdf_norm = p->z0_pdf_norm_thick;
        r0_pdf_norm = p->r0_pdf_norm_thick;
    }
    else{
        /* quit because we messed up, man! */
        fprintf(stderr, "Unrecognized disk type. Exiting.\n");
        exit(EXIT_FAILURE);
    }

    /* make stars until we have enough for this disk */
    for( i=0; i<N_stars; i++ ){

        /* Make sure we only get stars in the 1-3 kpc range */
        /* We don't wanna waste no FLOPS */
        flag = 0;
        while(flag==0){
            Z_temp   = random_gal_Z(z0, z0_pdf_norm, p->z_min);
            R_temp   = random_gal_R(r0, r0_pdf_norm, p->r_min);
            phi_temp = ( ( (double)rand() / (double)RAND_MAX )
                * p->phi_range + p->phi_min );
            dist_temp = get_distance(Z_temp, R_temp, phi_temp);

            /* Break out of while loop if condition is met */
            if( (dist_temp >= 1.0) && (dist_temp <= 3.0) ) flag = 1;
            if(dist_temp <= 3.0) flag = 1;
        }

        /* assign temp values to mock galaxy */
        s[i].gal_z    = Z_temp;
        s[i].gal_r    = R_temp;
        s[i].gal_phi  = phi_temp;
        s[i].distance = dist_temp;
    }

    /* vectorize with icc!! FAST! OMG!! */
    /* calculate the remaining star attributes */
    #pragma simd
    for( i=0; i<N_stars; i++ ){
        ZR_to_gal(&s[i]);
        gal_to_eq(&s[i]);
        eq_to_cart(&s[i]);
    }
}

/*---------------------------------------------------------------------------*/
