#include "config.h"

/* Return a galactic height */
long double random_gal_Z(long double z0, long double pdf_norm, long double z_min, long double z_max)
{
    long double cdf, b, temp, z, plus_minus;

    cdf = (long double)rand() / (long double)RAND_MAX;
    b = tanh( z_min / (2.0 * z0) );
    temp = ( cdf / (pdf_norm * 2.0 * z0) ) + b;
    z = atanh(temp) * 2.0 * z0;

    /* Generate + or - 1.0 */
    plus_minus = floor( 2.0 * (long double)rand() / (long double)RAND_MAX );
    plus_minus = plus_minus * 2.0 - 1.0;

    z *= plus_minus;
    return z;
}

/*---------------------------------------------------------------------------*/

/* Return distance in galactic plane */
long double random_gal_R(long double r0, long double pdf_norm, long double r_min, long double r_max)
{
    long double cdf, b, exp_term, r;

    cdf = (long double)rand() / (long double)RAND_MAX;
    b = exp(-r_min / r0);
    exp_term = b - ( cdf / (pdf_norm * r0) );
    r = -r0 * log(exp_term);

    return r;
}

/*---------------------------------------------------------------------------*/