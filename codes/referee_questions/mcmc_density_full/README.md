Make a single mock from a particular number of stars.
Assign all existing starsto appropriate l.o.s.
Fill each l.o.s. with uniform points.
Divide l.o.s. into segments.
Calculate mock density in each volume (N_points/volume).
Normalize this density by the average density in the entire l.o.s.

MCMC:
Weight uniform points according to the density at their Z, R positions.
Calculate average density (average of these weights).
Divide by average density in entire l.o.s.
Compare to mock density and accept or reject.

Notes:
Errors are from 1000 mocks.
Let's consider only errors on mock.