#include "config.h"

/*---------------------------------------------------------------------------*/

int main( int argc, char **argv ){

    if (argc != 2){
        fprintf( stderr, "Error. Usage: %s num_stars\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    unsigned long int N_stars;
    sscanf(argv[1], "%lu", &N_stars);

    fprintf(stderr, "%lu stars per temporary galaxy.\n", N_stars);


    POINTING *plist;
    int N_plist, loop_flag, pointings_in_need;
    PARAMS thin_params;
    PARAMS thick_params;
    time_t t;
    load_pointing_list(&N_plist, &plist);

    get_thin_params(&thin_params, N_stars);
    get_thick_params(&thick_params, N_stars);

    /* Allocate arrays for galactic coordinates */
    STAR * thin = malloc(thin_params.N_stars * sizeof(STAR));
    STAR * thick = malloc(thick_params.N_stars * sizeof(STAR));

    srand((unsigned) time(&t));

    generate_stars(thin, &thin_params);
    generate_stars(thick, &thick_params);

    char filename[256];
    FILE *file;


    // thin disk
    snprintf(filename, 256, "%smock_thin.dat", OUT_DIR);



    file = fopen(filename, "w");

    unsigned long int i;
    for(i=0; i<thin_params.N_stars; i++){
        fprintf( file, "%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\n",
            thin[i].gal_z, thin[i].gal_r, thin[i].gal_phi,
            thin[i].gal_l_rad, thin[i].gal_b_rad,
            thin[i].ra_rad, thin[i].dec_rad, thin[i].distance,
            thin[i].x, thin[i].y, thin[i].z );
    }

    fclose(file);


    // thick disk
    snprintf(filename, 256, "%smock_thick.dat", OUT_DIR);

    file = fopen(filename, "w");
    for(i=0; i<thick_params.N_stars; i++){
        fprintf( file, "%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\t%lf\n",
            thick[i].gal_z, thick[i].gal_r, thick[i].gal_phi,
            thick[i].gal_l_rad, thick[i].gal_b_rad,
            thick[i].ra_rad, thick[i].dec_rad, thick[i].distance,
            thick[i].x, thick[i].y, thick[i].z );
    }

    fclose(file);

    // loop_flag = 0;

    // int N_mock, N_data, i;
    // int loop_counter = 0;
    // while(loop_flag==0){
    //     pointings_in_need = 0;
    //     loop_flag = 1;
    //     generate_stars(thin, &thin_params);
    //     generate_stars(thick, &thick_params);
    //     separate_sample(plist, thin, N_plist, thin_params.N_stars);
    //     separate_sample(plist, thick, N_plist, thick_params.N_stars);

    //     for( i=0; i<N_plist; i++ ){
    //         N_mock = plist[i].N_mock;
    //         N_data = plist[i].N_data;

    //         if(N_mock<N_data){
    //             loop_flag = 0;
    //             plist[i].flag = 0;
    //             // fprintf(stderr, "Need to make more stars for pointing %s\n", plist[i].ID);
    //             // fprintf(stderr, "Mock: %d. Data: %d.\n", N_mock, N_data);
    //             pointings_in_need += 1;
    //         }
    //         else{
    //             plist[i].flag = 1;
    //         }
    //     }
    //     loop_counter +=1;
    //     fprintf(stderr, "We've run the loop %d times.\n", loop_counter);
    //     if (pointings_in_need != 0){
    //         fprintf(stderr, "%d pointings need more stars.\n", pointings_in_need);
    //         fprintf(stderr, "Making more stars. \n");
    //     }
    //     else fprintf(stderr, "All poitings have an adequate number of stars. \n");
    // }


    /* Deallocate arrays */
    free(thin);
    free(thick);
    fprintf(stderr, "Files Written. Arrays deallocated.\n");


    return 0;
}

/*---------------------------------------------------------------------------*/
