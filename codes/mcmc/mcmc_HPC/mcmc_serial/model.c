/* functions to calculate the number densities for a given galactic model */
#include "config.h"

/* number density of thin disk */
double thindisk_density(PARAMETERS p, double r, double z){

  double density;

  if(p.thindisk_type == 0){
    density = 0.0;
  }
  else if (p.thindisk_type == 1){
    density = p.thindisk_n0 * sech2(z / 2.0 / p.thindisk_z0) * exp(-r / p.thindisk_r0);
  }
  else{
    fprintf(stderr, "Error: Unknown Thin Disk Type. Type = %d.\n", p.thindisk_type);
    exit(EXIT_FAILURE);
  }

  return density;
}

/* number density of thick disk */
double thickdisk_density(PARAMETERS p, double r, double z){

  double density;

  if(p.thickdisk_type == 0){
    density = 0.0;
  }
  else if (p.thickdisk_type == 1){
    density = p.thickdisk_n0 * sech2(z / 2.0 / p.thickdisk_z0) * exp(-r / p.thickdisk_r0);
  }
  else{
    fprintf(stderr, "Error: Unknown Thick Disk Type. Type = %d.\n", p.thickdisk_type);
    exit(EXIT_FAILURE);
  }

  return density;
}

/* number density of halo */
double halo_density(PARAMETERS p, double r, double z){

  double density;
  double R = sqrt(r * r + z * z); /* convert cylindrical to spherical */

  if(p.halo_type == 0){
    density = 0.0;
  }
  else if (p.halo_type == 1){ /* spherically symmetry halo, no dependence on z */
    density = p.halo_n0 / pow((1.0 + R / p.halo_scaleradius), p.halo_innerslope);
  }
  else{
    fprintf(stderr, "Error: Unknown Halo Type. Type = %d.\n", p.halo_type);
    exit(EXIT_FAILURE);
  }

  return density;

}


/* Total number density of all components. */
double total_density(PARAMETERS p, double r, double z){

  /* if there are no parameters, return 1.0, thus no weights */
  if(p.N_parameters == 0){
    return 1.0;
  }

  double density = (thindisk_density(p, r, z)
		    + thickdisk_density(p, r, z)
		    + halo_density(p, r, z)
		    );

  return density;
}


void set_weights(PARAMETERS params, POINTING *plist, int N_plist){

  int i, j;
  double R, Z;

  /* loop over the Pointing list */
  for(i = 0; i < N_plist; i++){

    /* Set number densities as weights to the model stars. */
    for(j = 0; j < plist[i].N_model; j++){
      R = plist[i].model[j].galactic_R;
      Z = plist[i].model[j].galactic_Z;
      plist[i].model[j].weight = total_density(params, R, Z);
    }

    /* weights tests -- can be deleted later */
    /* char output_filename[256]; */
    /* FILE *output_file; */
    /* snprintf(output_filename, 256, "./tmp/star_%s.tmp.dat", plist[i].ID); */
    /* output_file = fopen(output_filename, "w"); */
    /* for(j = 0; j < plist[i].N_model; j++){ */
    /*   double x,y,z,w,gl,gb,gz,gr; */
    /*   x = plist[i].model[j].x; */
    /*   y = plist[i].model[j].y; */
    /*   z = plist[i].model[j].z; */
    /*   gl = plist[i].model[j].galactic_l_rad; */
    /*   gb = plist[i].model[j].galactic_b_rad; */
    /*   gz= plist[i].model[j].galactic_Z; */
    /*   gr = plist[i].model[j].galactic_R; */
    /*   w = plist[i].model[j].weight; */
    /*   fprintf(output_file, "%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%le\n", */
    /* 	      x, y, z, gl, gb, gz, gr, w); */
    /* } */
    /* fclose(output_file); */

  }

}
