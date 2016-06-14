#include "mcmc.h"

/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */
/* ------------------  Functions calculating errors  --------------------- */
/* ----------------------------------------------------------------------- */
/* ----------------------------------------------------------------------- */


/* ----------------------------------------------------------------------- */

/* Calculate fractional error in correlation */
void calculate_frac_error(MODEL *m, int N_bins){

    int j;

    for(j = 0; j < N_bins; j++){

        /* Multiply this by (DD/MM)**2 to get sigma**2 */
        if(m->rbin[j].DD_err_jk == 0.0 || m->rbin[j].MM_err_jk == 0.0){
            m->rbin[j].err2_frac = 0.0;
        }
        else{
            m->rbin[j].err2_frac = (
                m->rbin[j].DD_err_jk * m->rbin[j].DD_err_jk
                + m->rbin[j].MM_err_jk * m->rbin[j].MM_err_jk );
        }
    }

}

/* ----------------------------------------------------------------------- */

/* Calculate chi2 for a process's bin */
double calculate_chi2(MODEL *m, int rank){

    double chi2;

    /* multiplying by fractional error */
    m->rbin[rank].sigma2 = ( m->rbin[rank].corr * m->rbin[rank].corr *
        m->rbin[rank].err2_frac );

    /* ignore lines of sight with 0 counts */
    if( m->rbin[rank].sigma2 == 0.0 ){
        chi2 = 0.0;
    }
    else{
        chi2 += ( ( m->rbin[rank].corr - 1.0 ) * ( m->rbin[rank].corr - 1.0 )
            / m->rbin[rank].sigma2 );
    }

    return chi2;
}

/* ----------------------------------------------------------------------- */
