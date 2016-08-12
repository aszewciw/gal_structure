# Calculate the sigmas to be used in the MCMC chain.

## We take the following steps:

* First calculate normalized RR once for the uniform points.
* Read in the 1000 mock measurements of normalized DD.
* Calculate the covariance matrix of DD/RR within a single pointing.
* Output a file for each pointing containing this Nbins by Nbins matrix.