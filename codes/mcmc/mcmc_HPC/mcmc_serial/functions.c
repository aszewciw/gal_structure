#include "config.h"


/* Galactic North Pole in J2000, in degrees! */
const double Galactic_North_Pole_RA = 192.859508;
const double Galactic_North_Pole_Dec = 27.128336;
const double Galactic_Ascending_Node = 32.932;
/* Default Sun's position */
const double Sun_R = 8.0;
const double Sun_Z = 0.02;

double sech2(double x){
  return 1.0 / (cosh(x) * cosh(x));
}

/* update star's (x, y, z) using (ra, dec, distance)  */
void eq2cart(STAR *s){
  s->x = s->distance * cos(s->ra_rad) * cos(s->dec_rad);
  s->y = s->distance * sin(s->ra_rad) * cos(s->dec_rad);
  s->z = s->distance * sin(s->dec_rad);
}

/* update star's (ra, dec, distance) using (x, y, z) */
void cart2eq(STAR *s){
  s->distance = sqrt(s->x * s->x + s->y * s->y + s->z * s->z);
  s->ra_rad = atan2(s->y, s->x);
  if(s->ra_rad < 0){
    s->ra_rad = 2.0 * PI + s->ra_rad;
  }
  s->dec_rad = asin(s->z / s->distance);
}

/* update star's Galactic (l, b) using (ra, dec)  */
void eq2gal(STAR *s){
  double alpha, delta, la;
  /* convert params to radians */
  alpha = Galactic_North_Pole_RA * PI / 180.0;
  delta = Galactic_North_Pole_Dec * PI / 180.0;
  la = Galactic_Ascending_Node * PI / 180.0;

  double ra, dec, l, b; 	/* temporary holders*/
  ra = s->ra_rad;
  dec = s->dec_rad;

  b = asin(sin(dec) * sin(delta) +
	   cos(dec) * cos(delta) * cos(ra - alpha));

  l = atan2(sin(dec) * cos(delta) - cos(dec) * sin(delta) * cos(ra - alpha),
	    cos(dec) * sin(ra - alpha)
	    ) + la;

  if(l < 0) l += 2.0 * PI;
  
  l = fmod(l, (2.0 * PI));

  s->galactic_l_rad = l;
  s->galactic_b_rad = b;

}

/* update star's (ra, dec) using Galactic (l, b) */
void gal2eq(STAR *s){
  double alpha, delta, la;
  /* convert params to radians */
  alpha = Galactic_North_Pole_RA * PI / 180.0;
  delta = Galactic_North_Pole_Dec * PI / 180.0;
  la = Galactic_Ascending_Node * PI / 180.0;

  double ra, dec, l, b; 	/* temporary holders*/
  l = s->galactic_l_rad;
  b = s->galactic_b_rad;

  dec = asin(sin(b) * sin(delta) +
	     cos(b) * cos(delta) * sin(l - la));

  ra = atan2(cos(b) * cos(l - la),
	     sin(b) * cos(delta) - cos(b) * sin(delta) * sin(l - la)
	     ) + alpha;
  
  if(ra < 0) ra += 2.0 * PI;
  
  ra = fmod(ra, (2.0 * PI));

  s->ra_rad = ra;
  s->dec_rad = dec;

}

/* update Galactic (Z, R) */
/* This may depend on Sun's position! */
void gal2ZR(STAR *s, PARAMETERS params){

  double sr, sz;
  if(params.sun_position == 1){
    sr = params.sun_R;
    sz = params.sun_Z;
  }
  else{
    sr = Sun_R;
    sz = Sun_Z;
  }
  
  s->galactic_Z = fabs(s->distance * sin(s->galactic_b_rad) + sz);
  double x, y;
  x = s->distance * cos(s->galactic_b_rad);
  y = sr;
  s->galactic_R = (x * x + y * y 
		   - 2.0 * x * y * cos(s->galactic_l_rad));
  
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



