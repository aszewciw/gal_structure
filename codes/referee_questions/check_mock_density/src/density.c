#include "config.h"

/* randomly choose a volume element */
void get_volume(DVOL *dv, PARAMS *p){

    /* make sure volume element is within sample limits */
    int flag = 0;
    /* "size" of volume element */
    double dr, dz, dphi;
    double fraction; /* fraction of whole range to make each sub-element */
    /* temporary holders */
    double r_min, r_max, z_min, z_max, phi_min, phi_max;
    double volume;

    fraction = 0.01; /* trial and error here */

    dr   = (p->r_max - p->r_min) * fraction;
    dz   = (p->z_max - p->z_min) * fraction;
    dphi = (p->phi_max - p->phi_min) * fraction;

    /* choose random sections to test volume */
    /* make sure section actually exisits in full volume */
    while(flag==0){

        /* Assume everything works out for us */
        flag = 1;

        /* choose random min values */
        r_min   = (double)rand() / (double)RAND_MAX;
        r_min   = p->r_min + r_min * (p->r_max - p->r_min);
        z_min   = (double)rand() / (double)RAND_MAX;
        z_min   = p->z_min + z_min * (p->z_max - p->z_min);
        phi_min = (double)rand() / (double)RAND_MAX;
        phi_min = p->phi_min + phi_min * (p->phi_max - p->phi_min);

        /* add to min's to get max's */
        r_max   = r_min + dr;
        z_max   = z_min + dz;
        phi_max = phi_min + dphi;

        /* check if we're outside sample limits */
        /* Note: min values are by default within limits */
        if(r_max > p->r_max) flag = 0;
        if(z_max > p->z_max) flag = 0;
        if(phi_max > p->phi_max) flag = 0;
    }

    /* Integrate over cylindrical slice to get volume */
    volume = ( (phi_max - phi_min) * ( 0.5 * (r_max*r_max - r_min*r_min) )
        * (z_max - z_min) );

    /* assign values to main function arguments */
    dv->r_min     = r_min;
    dv->r_max     = r_max;
    dv->z_min     = z_min;
    dv->z_max     = z_max;
    dv->phi_min   = phi_min;
    dv->phi_max   = phi_max;
    dv->phi_range = phi_max - phi_min;
    dv->volume    = volume;
}

/* ---------------------------------------------------------------- */

/* return integral of sech^2(-z/(2*z0)) from z_min to z_max */
double integrate_Z_term(double z0, double z_min, double z_max){

    /* integral of sech^2(Z) term */
    double Z_integrated;

    Z_integrated = 2.0 * z0 * ( tanh( z_max / (2.0*z0) )
        - tanh( z_min / (2.0*z0) ) );

    return Z_integrated;
}

/* ---------------------------------------------------------------- */

/* return integral of r*exp(-r/r0) from r_min to r_max */
/* Note: extra "r" is due to Jacobian */
double integrate_R_term(double r0, double r_min, double r_max){

    /* integral of exp(-R) term */
    double R_integrated;

    R_integrated = -r0 * ( exp(-r_max/r0) * (r0 + r_max)
        - exp(-r_min/r0) * (r0 + r_min) );

    return R_integrated;
}

/* ---------------------------------------------------------------- */

/* Analytic average density of a given sample */
double ave_dens_analytic(PARAMS *p, DVOL *dv, unsigned long int N_stars){

    /* volume and average density */
    double density;
    /* geometric limits of volume element */
    double r_min, r_max, z_min, z_max, phi_min, phi_max, phi_range;
    /* volume of volume element */
    double volume;

    /* First assign limits from DVOL */
    r_min     = dv->r_min;
    r_max     = dv->r_max;
    z_min     = dv->z_min;
    z_max     = dv->z_max;
    phi_min   = dv->phi_min;
    phi_max   = dv->phi_max;
    phi_range = dv->phi_range;
    volume    = dv->volume;

    /* Now normalize the density */
    /* Note: normalization requires full volume (from PARAMS) */
    double Z_integrated;        /* integral of sech^2(Z) term */
    double R_integrated;        /* integral of exp(-R) term */
    double thin_term;           /* combined integral term for thin disk */
    double thick_term;          /* combined integral term for thick disk */
    long double density_const;  /* normalization of density */

    /* term for thin disk */
    Z_integrated = 2.0 * integrate_Z_term(p->z0_thin, p->z_min, p->z_max);
    R_integrated = integrate_R_term(p->r0_thin, p->r_min, p->r_max);
    thin_term    = Z_integrated * R_integrated * p->phi_range;

    /* term for thick disk */
    Z_integrated = 2.0 * integrate_Z_term(p->z0_thick, p->z_min, p->z_max);
    R_integrated = integrate_R_term(p->r0_thick, p->r_min, p->r_max);
    thick_term   = p->ratio * Z_integrated * R_integrated * p->phi_range;

    /* find normalization constant */
    density_const = (long double)N_stars / (thin_term + thick_term);

    /* Now get average density */
    /* Integrate density over wedge volume and divide by wedge volume */
    /* Note: this is a different volume than that used above */
    /* thin term */
    Z_integrated = integrate_Z_term(p->z0_thin, z_min, z_max);
    R_integrated = integrate_R_term(p->r0_thin, r_min, r_max);
    thin_term    = Z_integrated * R_integrated * phi_range;

    /* thick term */
    Z_integrated = integrate_Z_term(p->z0_thick, z_min, z_max);
    R_integrated = integrate_R_term(p->r0_thick, r_min, r_max);
    thick_term   = p->ratio * Z_integrated * R_integrated * phi_range;

    density = density_const * ( thin_term + thick_term ) / volume;

    return density;
}

/* ---------------------------------------------------------------- */

/* Average density of created mock */
double ave_dens_sample(PARAMS *p, DVOL *dv, STAR *thin, STAR *thick){

    /* volume and average density */
    double density;
    /* geometric limits of volume element */
    double r_min, r_max, z_min, z_max, phi_min, phi_max, phi_range;
    /* volume of volume element */
    double volume;
    /* for loop dummy */
    unsigned long int i;
    /* number of stars in volume element */
    double N_sample;
    N_sample = 0.0;

    /* First assign limits from DVOL */
    r_min     = dv->r_min;
    r_max     = dv->r_max;
    z_min     = dv->z_min;
    z_max     = dv->z_max;
    phi_min   = dv->phi_min;
    phi_max   = dv->phi_max;
    phi_range = dv->phi_range;
    volume    = dv->volume;

    /* count how many stars fall in volume element */

    /* thin disk first */
    #pragma simd
    for(i=0; i<p->N_thin; i++){

        /* skip if coordinates are outside of range */
        if( (thin[i].gal_z < z_min) || (thin[i].gal_z > z_max) ){
            continue;
        }
        if( (thin[i].gal_r < r_min) || (thin[i].gal_r > r_max) ){
            continue;
        }
        if( (thin[i].gal_phi < phi_min) || (thin[i].gal_phi > phi_max) ){
            continue;
        }

        /* if we haven't skipped then star is within element */
        N_sample += 1.0;
    }

    /* thick disk next */
    #pragma simd
    for(i=0; i<p->N_thick; i++){

        /* skip if coordinates are outside of range */
        if( (thick[i].gal_z < z_min) || (thick[i].gal_z > z_max) ){
            continue;
        }
        if( (thick[i].gal_r < r_min) || (thick[i].gal_r > r_max) ){
            continue;
        }
        if( (thick[i].gal_phi < phi_min) || (thick[i].gal_phi > phi_max) ){
            continue;
        }

        /* if we haven't skipped then star is withick element */
        N_sample += 1.0;
    }

    /* get average density in this region */
    density = N_sample / volume;

    return density;
}