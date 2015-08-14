/* Calculates the correlation function
between data points and random points.

My working c correlation function, heavily based on
Qingqing's.
*/

#include <stdlib.h>
#include <stdio.h>
#include <math.h>

typedef struct {
    double x, y, z, weight;
} point;

typedef struct {
    int N;
    point *points;
} DATA;

int count_pairs(struct DATA, int rmin, int rmax) {
    /*Code to count number of pairs in each bin*/
}

int main(int argc, char **argv) {
    /*Put some things in here*/

    //Not sure how data will be loaded but let's assume it's here
    /*Let's just structure it like QQ did. Arguments will be:
    0. correlation file name
    1. data file name
    2. random/model file name
    3. min bin size
    4. max bin size
    5. number of bins
    */

    //Variable declarations
    double bin_min, bin_max;
    int N_bins;            //Why do unsigned vs signed?
    sscanf(argv[3], "%lf", &bin_min);
    sscanf(argv[4], "%lf", &bin_max);
    sscanf(argv[5], "%d", &N_bins);

    double rmax_log, rmin_log, dr_log;
    rmax_log = log(rmax) / log(10.0);
    rmin_log = log(rmin) / log(10.0);
    dr_log = (rmax_log - rmin_log) / nbins;




}