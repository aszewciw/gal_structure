Make a single mock from a particular number of stars.
Assign all existing starsto appropriate l.o.s.
Fill each l.o.s. with uniform points.
Divide l.o.s. into segments.
Calculate mock density in each volume (N_points/volume).

MCMC:
Weight uniform points according to the density at their Z, R positions.
Calculate average density (average of these weights).
Compare to mock density and accept or reject.

Notes:
Errors will just be Poisson.
Let's consider only errors on mock.