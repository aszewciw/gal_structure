#include <math.h>
#include <time.h>

#include "config.h"

double sech2(double x){
  return 1.0 / (cosh(x) * cosh(x));
}

void eq2cart(STAR *s){
  
  s->x = s->distance * cos(s->ra_rad) * cos(s->dec_rad);
  s->y = s->distance * sin(s->ra_rad) * cos(s->dec_rad);
  s->z = s->distance * sin(s->dec_rad);

}

void cart2eq(STAR *s){
  
  s->distance = sqrt(s->x * s->x + s->y * s->y + s->z * s->z);
  s->ra_rad = atan2(s->y, s->x);
  if(s->ra_rad < 0){
    s->ra_rad = 2.0 * PI + s->ra_rad;
  }
  s->dec_rad = asin(s->z / s->distance);

}

/* Dot product of 2 vectors in 3D cartesian space. */
double dot(VECTOR vec1, VECTOR vec2){
  double dp;
  dp = vec1.x * vec2.x + vec1.y * vec2.y + vec1.z * vec2.z;
  return dp;
}

/* Cross product of 2 vectors in 3D Cartesian space. */
VECTOR cross(VECTOR vec1, VECTOR vec2){

  VECTOR result;
  result.x = vec1.y * vec2.z - vec1.z * vec2.y;
  result.y = vec1.z * vec2.x - vec1.x * vec2.z;
  result.z = vec1.x * vec2.y - vec1.y * vec2.x;

  return result;

}


/* This function rotate a vector around an axis in 3D Cartesian space
   using Rodrigues' rotation formula. 
*/
VECTOR rodrigues(VECTOR axis, VECTOR vec, double theta_rad){
  
  /* normalize the axis vector */
  double ar = sqrt(axis.x * axis.x + axis.y * axis.y + axis.z * axis.z);
  axis.x = axis.x / ar;
  axis.y = axis.y / ar;
  axis.z = axis.z / ar;

  /* cross product and dot product */
  VECTOR cp = cross(axis, vec);
  double dp = dot(axis, vec);

  VECTOR result;
  result.x = (vec.x * cos(theta_rad) + cp.x * sin(theta_rad)
	      + axis.x * dp * (1 - cos(theta_rad)));

  result.y = (vec.y * cos(theta_rad) + cp.y * sin(theta_rad)
	      + axis.y * dp * (1 - cos(theta_rad)));
  
  result.z = (vec.z * cos(theta_rad) + cp.z * sin(theta_rad)
	      + axis.z * dp * (1 - cos(theta_rad)));

  return result;

}



