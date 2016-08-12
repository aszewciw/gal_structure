// #include "mcmc.h"

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
// double calculate_chi2(POINTING *p, int N_bins, int lower_ind, int upper_ind){

//     int i, j;
//     double chi2 = 0.0;

//     for(i = lower_ind; i < upper_ind; i++){

//         for(j = 0; j < N_bins; j++){

//             /* multiplying by fractional error */
//             p[i].rbin[j].sigma2 = ( p[i].rbin[j].corr * p[i].rbin[j].corr *
//                 p[i].rbin[j].err2_frac );

//             /* ignore lines of sight with 0 counts */
//             if( p[i].rbin[j].sigma2 == 0.0 ) continue;

//             chi2 += ( ( p[i].rbin[j].corr - 1.0 ) * ( p[i].rbin[j].corr - 1.0 )
//                 / p[i].rbin[j].sigma2 );
//         }
//     }

//     return chi2;
// }

/* ----------------------------------------------------------------------- */
