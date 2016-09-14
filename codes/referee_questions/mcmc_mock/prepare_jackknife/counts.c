/*
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

typedef struct CORRELATION{
  double r_lower, r_upper, r_middle, bin_size;
  double r2_lower, r2_upper;
  long DD_N, MM_N;              /* raw number of pairs without weighting */
  double DD, MM;                /* weighted and normalized pair counts */
  double correlation;

} CORRELATION;
/* ------------------------------------------------------------------------- */



/* ------------------------------------------------------------------------- */
double pairs(POINT *data, int N_data, CORRELATION *corr, int N_corr){

  double r1, r2, dx, dy, dz, ds;

  int i, j, k;

  for(i = 0; i < N_data; i++){
    for(j = i + 1; j < N_data; j++){

      dx = data[i].x - data[j].x;
      dy = data[i].y - data[j].y;
      dz = data[i].z - data[j].z;

      ds = dx * dx + dy * dy + dz * dz; /* distance square */

      for(k = 0; k < N_corr; k++ ){
        r1 = corr[k].r2_lower;
        r2 = corr[k].r2_upper;
        if(ds >= r1 && ds < r2){
          corr[k].DD_N += 1;
          corr[k].DD += data[i].weight * data[j].weight;
          break;
        }
      }

    }
  }

  return 0;
}


int main(int argc, char **argv){

  if (argc != 3){
    fprintf( stderr, "Usage:\n %s data_file bins_file > outfile\n", argv[0]);
    exit(EXIT_FAILURE);
  }

  FILE *data_file;

  if((data_file=fopen(argv[1],"r"))==NULL){
    fprintf(stderr,"Error: Cannot open file %s \n", argv[1]);
    exit(EXIT_FAILURE);
  }

  FILE *bins_file;

  if((bins_file=fopen(argv[2],"r"))==NULL){
    fprintf(stderr,"Error: Cannot open file %s \n", argv[1]);
    exit(EXIT_FAILURE);
  }

  int nbins;
  fscanf(bins_file, "%d", &nbins);

  CORRELATION *corr;
  corr = calloc(nbins, sizeof(CORRELATION));

  int i, k;

  /*  read in bin settings and prepare corr*/
  for(k = 0; k < nbins; k++){
    fscanf(bins_file, "%lf", &corr[k].r_lower);
    fscanf(bins_file, "%lf", &corr[k].r_upper);
    fscanf(bins_file, "%lf", &corr[k].r_middle);
    fscanf(bins_file, "%lf", &corr[k].bin_size);
    corr[k].r2_lower = corr[k].r_lower * corr[k].r_lower;
    corr[k].r2_upper = corr[k].r_upper * corr[k].r_upper;
    corr[k].DD_N = 0;
    corr[k].MM_N = 0;
    corr[k].DD = 0.0;
    corr[k].MM = 0.0;
    corr[k].correlation = 0.0;
  }


  /* load data file */
  int N_data;
  POINT *data;

  fprintf(stderr, "data file is: %s\n", argv[1]);
  fprintf(stderr, "Reading data .. \n");

  fscanf(data_file, "%d", &N_data); /* first read in the length of the list */

  /* Claim an array for a list of pointing */
  data = calloc(N_data, sizeof(POINT));

  for(i = 0; i < N_data; i++){
    fscanf(data_file, "%lf", &data[i].x);
    fscanf(data_file, "%lf", &data[i].y);
    fscanf(data_file, "%lf", &data[i].z);
    fscanf(data_file, "%lf", &data[i].weight);
  }

  fprintf(stderr, "Read %d stars. \n", N_data);

  fclose(data_file);

  // calculate the correlation
  fprintf(stderr, "Start calculating the correlation function... \n");

  pairs(data, N_data, corr, nbins);


  /* output */
  for(k = 0; k < nbins; k++){
    fprintf(stdout, "%lf\t%lf\t%lf\t%lf\t%ld\t%le\n",
      corr[k].r_lower, corr[k].r_upper, corr[k].r_middle, corr[k].bin_size,
      corr[k].DD_N, corr[k].DD);
  }

  fprintf(stderr, "Done calculation and output. \n");


  return EXIT_SUCCESS;

}


// /*
//   For a given sample, find pair counts in various radial bins.
//   Output bin data and raw pair counts.
//   Marked pair counting is not done here.
// */

// /* ------------------------------------------------------------------------- */
// #include <stdlib.h>
// #include <stdio.h>
// #include <math.h>

// /* ------------------------------------------------------------------------- */
// /* structure used to store the data set of particles */
// typedef struct POINT{
//   double x,y,z; /* cartesian positions */
// } POINT;

// /* structure used to store bin, pair count data */
// typedef struct COUNTS{
//   double r_lower, r_upper, r_middle, bin_size;  /* bin limits */
//   double r2_lower, r2_upper;                    /* r^2 of bin */
//   long DD_raw;                                  /* raw pair counts */
// } COUNTS;
// /* ------------------------------------------------------------------------- */



// /* ------------------------------------------------------------------------- */
// void pairs(POINT *data, int N_data, COUNTS *corr, int N_corr){

//   /* temporary holders */
//   double r1, r2, dx, dy, dz, ds;

//   int i, j, k;

//   for(i = 0; i < N_data; i++){

//     for(j = i + 1; j < N_data; j++){

//       dx = data[i].x - data[j].x;
//       dy = data[i].y - data[j].y;
//       dz = data[i].z - data[j].z;

//       /* distance square */
//       ds = dx * dx + dy * dy + dz * dz;

//       /* Find appropriate radial bin and add to counts */
//       for(k = 0; k < N_corr; k++ ){

//         /* set squared limits */
//         r1 = corr[k].r2_lower;
//         r2 = corr[k].r2_upper;

//         /* check if a member of bin */
//         if(ds >= r1 && ds < r2){

//           corr[k].DD_raw += 1;

//           break;
//         }
//       }
//     }
//   }
// }


// int main(int argc, char **argv){

//   if (argc != 3){
//     fprintf( stderr, "Usage:\n %s data_file bins_file > outfile\n", argv[0]);
//     exit(EXIT_FAILURE);
//   }

//   FILE *data_file;

//   if((data_file=fopen(argv[1],"r"))==NULL){
//     fprintf(stderr,"Error: Cannot open file %s \n", argv[1]);
//     exit(EXIT_FAILURE);
//   }

//   FILE *bins_file;

//   if((bins_file=fopen(argv[2],"r"))==NULL){
//     fprintf(stderr,"Error: Cannot open file %s \n", argv[1]);
//     exit(EXIT_FAILURE);
//   }

//   int nbins;
//   fscanf(bins_file, "%d", &nbins);

//   COUNTS *corr;
//   corr = calloc(nbins, sizeof(COUNTS));

//   int i, k;

//   /*  read in bin settings and prepare corr*/
//   for(k = 0; k < nbins; k++){
//     fscanf(bins_file, "%lf", &corr[k].r_lower);
//     fscanf(bins_file, "%lf", &corr[k].r_upper);
//     fscanf(bins_file, "%lf", &corr[k].r_middle);
//     fscanf(bins_file, "%lf", &corr[k].bin_size);
//     corr[k].r2_lower = corr[k].r_lower * corr[k].r_lower;
//     corr[k].r2_upper = corr[k].r_upper * corr[k].r_upper;
//     corr[k].DD_raw = 0;
//   }


//   /* load data file */
//   int N_data;
//   POINT *data;

//   fprintf(stderr, "data file is: %s\n", argv[1]);
//   fprintf(stderr, "Reading data .. \n");

//   fscanf(data_file, "%d", &N_data); /* first read in the length of the list */

//   /* Claim an array for a list of pointing */
//   data = calloc(N_data, sizeof(POINT));

//   for(i = 0; i < N_data; i++){
//     fscanf(data_file, "%lf", &data[i].x);
//     fscanf(data_file, "%lf", &data[i].y);
//     fscanf(data_file, "%lf", &data[i].z);
//   }

//   fprintf(stderr, "Read %d stars. \n", N_data);

//   fclose(data_file);

//   // calculate the COUNTS
//   fprintf(stderr, "Start calculating the pair counts... \n");

//   pairs(data, N_data, corr, nbins);


//   /* output */
//   for(k = 0; k < nbins; k++){
//     fprintf(stdout, "%lf\t%lf\t%lf\t%lf\t%ld\n",
// 	    corr[k].r_lower, corr[k].r_upper, corr[k].r_middle, corr[k].bin_size,
// 	    corr[k].DD_raw);
//   }

//   fprintf(stderr, "Done calculation and output. \n");


//   return EXIT_SUCCESS;

// }
