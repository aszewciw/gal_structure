#include "mcmc.h"

/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* ------------------  Functions calculating errors  --------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */


/* ----------------------------------------------------------------------- */

/* Calculate chi2 for a process's given slice of pointings */
double calculate_chi2(POINTING *p, int N_bins, int lower_ind, int upper_ind){

    int i, j;
    double chi2 = 0.0;

    for(i = lower_ind; i < upper_ind; i++){

        for(j = 0; j < N_bins; j++){

            /* scale frac error by current model */
            p[i].rbin[j].sigma2 = ( p[i].rbin[j].MM * p[i].rbin[j].MM
                * p[i].rbin[j].frac_error * p[i].rbin[j].frac_error );

            /* ignore lines of sight with 0 counts */
            if( p[i].rbin[j].sigma2 == 0.0 ) continue;

            chi2 += ( ( p[i].rbin[j].DD - p[i].rbin[j].MM )
                * ( p[i].rbin[j].DD - p[i].rbin[j].MM )
                / p[i].rbin[j].sigma2 );
        }
    }

    return chi2;
}

/* ----------------------------------------------------------------------- */
