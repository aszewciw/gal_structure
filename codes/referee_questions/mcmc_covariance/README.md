# This will be a mock MCMC chain in which calculations of chi square include non-diagonal terms from the covariance matrix.

## The mock data places the same number of stars in each pointing as are in the SEGUE pointing.

## The covariance matrix is produced by finding the value of DD/RR for 1000 mocks (the DD pair counts).

## Covariance matrices are only considered within each pointing and not across pointings because these were deemed to be negligible.

*See the ipython notebook for more details