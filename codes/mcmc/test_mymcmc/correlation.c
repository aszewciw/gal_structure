/*
   Qingqing's code for correlation. My (working) version is based on this.
   Calculating the correlation function between data and random catalog.
   Directly pair counting is used.
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


/* ------------------------------------------------------------------------- */
double cross_pairs(DATA data1, DATA data2, double r1, double r2){

  double rs1 = r1 * r1;
  double rs2 = r2 * r2;

  double counts = 0.0;

  double dx, dy, dz, ds;

  int i, j;

  POINT p1, p2;

  for(i = 0; i < data1.N; i++){

    p1 = data1.points[i];

    for(j = 0; j < data2.N; j++){

      p2 = data2.points[j];

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
double cross_pairs_norm(DATA data1, DATA data2){

  double total = 0.0;
  int i, j;

  for(i = 0; i < data1.N; i++){
    for(j = 0; j < data2.N; j++){
      total += data1.points[i].weight * data2.points[j].weight;
    }
  }

  return total;
}


/* ------------------------------------------------------------------------- */
double self_pairs(DATA data, double r1, double r2){

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
double self_pairs_norm(DATA data){

  double total = 0.0;
  int i, j;

  for(i = 0; i < data.N; i++){
    for(j = i + 1; j < data.N; j++){
      total += data.points[i].weight * data.points[j].weight;
    }
  }

  return total;
}


/* ------------------------------------------------------------------------- */
double pairs(DATA data1, DATA data2, double r1, double r2){

  double counts;

  if(data1.points == data2.points)
    counts = self_pairs(data1, r1, r2);
  else
    counts = cross_pairs(data1, data2, r1, r2);

  return counts;

}

/* ------------------------------------------------------------------------- */
double pairs_norm(DATA data1, DATA data2){

  double total;

  if(data1.points == data2.points)
    total = self_pairs_norm(data1);
  else
    total = cross_pairs_norm(data1, data2);

  return total;

}



int main(int argc, char **argv){

  if (argc != 6){
    fprintf( stderr, "Usage:\n %s datafile randomfile r_min r_max r_bin> outfile\n", argv[0]);
    exit(EXIT_FAILURE);
  }

  FILE *file1, *file2;

  if((file1=fopen(argv[1],"r"))==NULL){
    fprintf(stderr,"Error: Cannot open file %s \n", argv[1]);
    exit(EXIT_FAILURE);
  }
  if((file2=fopen(argv[2],"r"))==NULL){
    fprintf(stderr,"Error: Cannot open file %s \n", argv[2]);
    exit(EXIT_FAILURE);
  }

  double rmin, rmax;
  int nbins;
  sscanf(argv[3], "%lf", &rmin);
  sscanf(argv[4], "%lf", &rmax);
  sscanf(argv[5], "%d", &nbins);

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

  fprintf(stderr, "data file is: %s\n random file is %s\n", argv[1], argv[2]);
  fprintf(stderr, "log(rmin) = %lf,\t log(rmax) = %lf,\t log(dr) = %f\n", rmin_log, rmax_log, dr_log);

  fprintf(stderr, "Start reading data and random. \n");

  int i;

  DATA data1, data2;

  //read in the data from stdin
  int Nfetch = 100000;

  unsigned long int n, np;

  // read in the data file
  n = Nfetch;
  data1.points = (POINT *)calloc(n, sizeof (POINT));

  i = 0;
  np = 0;
  while(fscanf(file1, "%lf", &data1.points[i].x) == 1){
    fscanf(file1, "%lf", &data1.points[i].y);
    fscanf(file1, "%lf", &data1.points[i].z);
    fscanf(file1, "%lf", &data1.points[i].weight);
    i++;
    np++;
    if(i == n){
      n += Nfetch;
      data1.points = (POINT *)realloc(data1.points, n * sizeof (POINT));
    }
  }

  data1.points = (POINT *)realloc(data1.points, np * sizeof (POINT));
  fprintf( stderr, "Done reading %s. %lu particles read. \n", argv[1], np );
  data1.N = np;

  // read in the random file
  n = Nfetch;
  data2.points = (POINT *)calloc(n, sizeof (POINT));

  i = 0;
  np = 0;
  while(fscanf(file2, "%lf", &data2.points[i].x) == 1){
    fscanf(file2, "%lf", &data2.points[i].y);
    fscanf(file2, "%lf", &data2.points[i].z);
    fscanf(file2, "%lf", &data2.points[i].weight);
    i++;
    np++;
    if(i == n){
      n += Nfetch;
      data2.points = (POINT *)realloc(data2.points, n * sizeof (POINT));
    }
  }

  data2.points = (POINT *)realloc(data2.points, np * sizeof (POINT));
  fprintf( stderr, "Done reading %s. %lu particles read. \n", argv[2], np );
  data2.N = np;

  // calculate the correlation
  fprintf(stderr, "Start calculating the correlation function... \n");
  double r_log;

  double DD_norm, RR_norm, DR_norm;
  DD_norm = pairs_norm(data1, data1);
  RR_norm = pairs_norm(data2, data2);
  DR_norm = pairs_norm(data1, data2);

  for(r_log = rmin_log; r_log <= rmax_log; r_log += dr_log){

    double DD, RR, DR;
    double correlation;

    double r1, r2;
    r1 = pow(10.0, r_log);
    r2 = pow(10.0, (r_log + dr_log));

    fprintf(stderr, "Calculating the bin %lf <= r < %lf ...\n", r1, r2);
    DD = pairs(data1, data1, r1, r2);
    RR = pairs(data2, data2, r1, r2);
    DR = pairs(data1, data2, r1, r2);

    //fprintf(stderr, "DD = %lf, \t RR = %lf, \t DR = %lf \n", DD, RR, DR);
    //fprintf(stderr, "DD_norm = %le, \t RR_norm = %le, \t DR_norm = %le \n",
    //         DD_norm, RR_norm, DR_norm);

    DD /= DD_norm;
    RR /= RR_norm;
    DR /= DR_norm;

    //correlation = (DD - 2 * DR + RR) / RR ;
    correlation = DD / RR - 1.0;

    // fprintf(stderr, "r = %lf, \tcorrelation = %lf\n", r1, correlation);

    fprintf(stdout, "%lf\t%lf\t%lf\t%le\t%le\t%le\t%le\n",
	    r1, correlation, pow(10.0, dr_log),
	    DD, DD_norm, RR, RR_norm);

  }

  fprintf(stderr, "Done calculation and output. \n");

  free(data1.points);
  free(data2.points);
  return 0;

}
