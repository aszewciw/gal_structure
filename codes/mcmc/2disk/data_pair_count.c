/*
    Counts all data pairs for each los (152) and each bin in r (12). Data fed
    to this file are the SEGUE data file, bin_min, bin_max, N_bins. File counts
    pairs DD. Output is raw pair counts, normalization factor, and normalized
    pair counts
*/

#include <stdlib.h>
#include <stdio.h>
#include <math.h>

/* ------------------------------------------------------------------------- */
/* structure used to store the data set of particles */
typedef struct POINT{
  double x,y,z;
  double weight;
} POINT;

typedef struct DATA{
  unsigned int N;
  POINT *points;
} DATA;
/* ------------------------------------------------------------------------- */

double pairs(DATA data, double r1, double r2){

  double rs1 = r1 * r1;
  double rs2 = r2 * r2;

  double counts = 0.0;

  double dx, dy, dz, ds;

  int i, j;

  POINT p1, p2;

  for(i = 0; i < data.N; i++){

    p1 = data.points[i];

    for(j = i + 1; j < data.N; j++){

      p2 = data.points[j];

      dx = fabs(p1.x - p2.x);
      if(dx >= r2) continue;

      dy = fabs(p1.y - p2.y);
      if(dy >= r2) continue;

      dz = fabs(p1.z - p2.z);
      if(dz >= r2) continue;

      ds = dx * dx + dy * dy + dz * dz; /* distance square */

      if(ds >= rs1 && ds < rs2)
  counts += p1.weight * p2.weight;

    }
  }

  return counts;
}

/* ------------------------------------------------------------------------- */

double pairs_norm(DATA data){

  double total = 0.0;
  int i, j;

  for(i = 0; i < data.N; i++){
    for(j = i + 1; j < data.N; j++){
      total += data.points[i].weight * data.points[j].weight;
    }
  }

  return total;
}


int main(int argc, char **argv){

  if (argc != 5){
    fprintf( stderr, "Usage:\n %s data_file r_min r_max N_bins > outfile\n", argv[0]);
    exit(EXIT_FAILURE);
  }

  FILE *file;

  if((file=fopen(argv[1],"r"))==NULL){
    fprintf(stderr,"Error: Cannot open file %s \n", argv[1]);
    exit(EXIT_FAILURE);
  }

  double rmin, rmax;
  int nbins;
  sscanf(argv[2], "%lf", &rmin);
  sscanf(argv[3], "%lf", &rmax);
  sscanf(argv[4], "%d", &nbins);

  if(rmin >= rmax){
    fprintf(stderr,
      "Error: rmin is greater than rmax. Nothing will be calculated. \n");
    exit(EXIT_FAILURE);
  }

  if(rmin == 0){
    rmin = 1e-3;
    fprintf(stderr, "Warning: Input rmin is 0, so it is set to 1e-3. \n");
  }

  if(nbins <= 0){
    fprintf(stderr,
      "Error: nbins is not positive. No bin will be calculated. \n");
    exit(EXIT_FAILURE);
  }

  double rmax_log, rmin_log, dr_log;

  rmax_log = log(rmax) / log(10.0);
  rmin_log = log(rmin) / log(10.0);
  dr_log = (rmax_log - rmin_log) / nbins;

  fprintf(stderr, "data file is: %s\n", argv[1]);
  fprintf(stderr, "log(rmin) = %lf,\t log(rmax) = %lf,\t log(dr) = %f\n", rmin_log, rmax_log, dr_log);

  fprintf(stderr, "Start reading data and random. \n");

  int i;

  DATA data;

  //read in the data from stdin
  int Nfetch = 100000;

  unsigned long int n, np;

  // read in the data file
  n = Nfetch;
  data.points = (POINT *)calloc(n, sizeof (POINT));

  i = 0;
  np = 0;
  while(fscanf(file, "%lf", &data.points[i].x) == 1){
    fscanf(file, "%lf", &data.points[i].y);
    fscanf(file, "%lf", &data.points[i].z);
    fscanf(file, "%lf", &data.points[i].weight);
    i++;
    np++;
    if(i == n){
      n += Nfetch;
      data.points = (POINT *)realloc(data.points, n * sizeof (POINT));
    }
  }

  data.points = (POINT *)realloc(data.points, np * sizeof (POINT));
  fprintf( stderr, "Done reading %s. %lu particles read. \n", argv[1], np );
  data.N = np;


  // calculate the correlation
  fprintf(stderr, "Start counting data pairs... \n");
  double r_log;

  double DD_norm;
  DD_norm = pairs_norm(data);

  for(r_log = rmin_log; r_log < rmax_log; r_log += dr_log){

    double DD, DD_N, r1, r2;

    r1 = pow(10.0, r_log);
    r2 = pow(10.0, (r_log + dr_log));

    fprintf(stderr, "Calculating the bin %lf <= r < %lf ...\n", r1, r2);
    DD = pairs(data, r1, r2);
    DD_N = DD / DD_norm;

    fprintf(stdout, "%lf\t%lf\t%lf\n", DD, DD_norm, DD_N);
  }

  fprintf(stderr, "Done calculation and output. \n");

  free(data.points);
  return 0;

  return EXIT_SUCCESS;

}
