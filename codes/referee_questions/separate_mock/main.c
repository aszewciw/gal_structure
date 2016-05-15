#include "config.h"

/* dot product of two unit vectors */
long double dot_product(VECTOR v1, VECTOR v2){
    long double dot;

    dot = v1.x * v2.x + v1.y * v2.y + v1.z * v2.z;

    return dot;
}

void separate_sample(POINTING *p, STAR *s, int N_p, unsigned long int N_s){
    int i;
    unsigned long int j;
    char filename[256];
    FILE *file;
    VECTOR plate, point;
    long double dot_prod;
    long double plate_cos;
    int star_count;

    plate_cos = cos( PLATE_RADIUS_DEG * M_PI / 180. );

    for(i=0; i<N_p; i++){
        snprintf(filename, 256, "%smock_%s.xyz.dat", OUT_DIR, p[i].ID);
        file = fopen(filename, "a");
        star_count = 0;

        /* plate unit vector */
        plate.x = p[i].x;
        plate.y = p[i].y;
        plate.z = p[i].z;

        for(j=0; j<N_s; j++){

            /* unit vectors */
            point.x = s[j].x / s[j].distance;
            point.y = s[j].y / s[j].distance;
            point.z = s[j].z / s[j].distance;

            dot_prod = dot_product(plate, point);

            if(dot_prod >= plate_cos){
                star_count += 1;
                fprintf( file, "%Lf\t%Lf\t%Lf\n", s[j].x, s[j].y, s[j].z );
            }
        }
        p[i].N_mock += star_count;
        fclose(file);
    }
}
/* ----------------------------------------------------------------------- */

int main(int argc, char * argv[]){

    POINTING *plist;
    STAR *thin;
    STAR *thick;
    int N_plist;
    unsigned long int N_stars_thin, N_stars_thick;

    load_pointing_list(&N_plist, &plist);

    load_mock_thin(&N_stars_thin, &thin);
    load_mock_thick(&N_stars_thick, &thick);

    separate_sample(plist, thin, N_plist, N_stars_thin);
    separate_sample(plist, thick, N_plist, N_stars_thick);

    //check all pointings
    int i, N_mock, N_data;
    int half;
    for(i=0; i<N_plist; i++){
        N_mock = plist[i].N_mock;
        N_data = plist[i].N_data;

        half = N_data / 2;

        // if(N_mock < N_data){
        //     fprintf(stderr, "Not enough stars for pointing %s\n", plist[i].ID);
        //     fprintf(stderr, "%d more stars needed.\n", N_data - N_mock);
        // }
        // if(N_mock==0){
        //     fprintf(stderr, "There are no stars for pointing %s\n", plist[i].ID);
        // }
        if(N_mock < 25){
            fprintf(stderr, "Less than 25 stars for pointing %s\n", plist[i].ID);
        }
        if(half>N_mock){
            fprintf(stderr, "Need to run more than twice for pointing %s\n", plist[i].ID);
        }
    }

    free(plist);
    free(thin);
    free(thick);
    fprintf(stderr, "Arrays deallocated.\n");

}
