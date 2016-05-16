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