#include "mcmc.h"

/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* ------------------  Functions calculating errors  --------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */


/* ----------------------------------------------------------------------- */

// /* Calculate fractional error in correlation */
// void calculate_frac_error(POINTING *p, int N_bins, int lower_ind, int upper_ind){

//     int i, j;

//     for(i = lower_ind; i < upper_ind; i++){

//         for(j = 0; j < N_bins; j++){

//             /* Multiply this by (DD/MM)**2 to get sigma**2 */
//             if(p[i].rbin[j].DD_err_jk == 0.0 || p[i].rbin[j].MM_err_jk == 0.0){
//                 p[i].rbin[j].err2_frac = 0.0;
//             }
//             else{
//                 p[i].rbin[j].err2_frac = (
//                     p[i].rbin[j].DD_err_jk * p[i].rbin[j].DD_err_jk
//                     + p[i].rbin[j].MM_err_jk * p[i].rbin[j].MM_err_jk );
//             }
//         }
//     }
// }

/* ----------------------------------------------------------------------- */

/* Calculate chi2 for a process's given slice of pointings */
double calculate_chi2(POINTING *p, int N_bins, int lower_ind, int upper_ind){

    int i, j, k;
    double chi2 = 0.0;

    /* loop over pointings */
    for(i = lower_ind; i < upper_ind; i++){

        /* loop over bin rows */
        for(j = 0; j < N_bins; j++){

            /* loop over bin columns */
            for(k=j; k<N_bins; k++){

                /* skip any 0 counts in DD, MM, RR, or covariance */
                if(p[i].rbin[j].DD_RR == 0.0 || p[i].rbin[j].MM_RR == 0.0){
                    continue;
                }
                if(p[i].rbin[k].DD_RR == 0.0 || p[i].rbin[k].MM_RR == 0.0){
                    continue;
                }
                if(p[i].cov_row[j].cov_col[k] == 0.0) continue;

                chi2 += p[i].rbin[j].diff * p[i].rbin[k].diff / p[i].cov_row[j].cov_col[k];

            }

        }
    }

    return chi2;
}

/* ----------------------------------------------------------------------- */
