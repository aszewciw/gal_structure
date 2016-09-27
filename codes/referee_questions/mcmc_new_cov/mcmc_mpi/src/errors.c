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

    int i, j, k;
    double chi2 = 0.0;
    double corr_model_j, corr_model_k;
    double corr_data_j, corr_data_k;
    double sigma_j, sigma_k;

    for(i = lower_ind; i < upper_ind; i++){

        /* loop over bin rows */
        for(j = 0; j < N_bins; j++){

            /* loop over bin column elements */
            for(k = 0; k < N_bins; k++){

                /* skip any bins where we have 0 counts */
                if( p[i].rbin[j].DD == 0.0 ) continue;
                if( p[i].rbin[j].MM == 0.0 ) continue;
                if( p[i].rbin[j].frac_error == 0.0 ) continue;
                if( p[i].rbin[k].DD == 0.0 ) continue;
                if( p[i].rbin[k].MM == 0.0 ) continue;
                if( p[i].rbin[k].frac_error == 0.0 ) continue;

                /* Set definitions for model and data */
                corr_model_j = p[i].rbin[j].MM;
                corr_data_j = p[i].rbin[j].DD;
                corr_model_k = p[i].rbin[k].MM;
                corr_data_k = p[i].rbin[k].DD;

                /* scale frac errors by current model to estimate real sigmas */
                sigma_j = ( corr_model_j * p[i].rbin[j].frac_error );
                sigma_k = ( corr_model_k * p[i].rbin[k].frac_error );

                /* add contribution to covariance matrix */
                chi2 += ( ( ( corr_data_j - corr_model_j ) / sigma_j )
                    * ( ( corr_data_k - corr_model_k ) / sigma_k )
                    * p[i].invcor_row[j].invcor_col[k] );
            }

        }
    }

    return chi2;
}

/* ----------------------------------------------------------------------- */
