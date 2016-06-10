The details for this folder are as follows:

I create a mock according to some density function in R and Z.
The function will consist of a sum of two distributions to
mock the thin and thick disks of the galaxy. However, the
function will not be of the form as those galactic disks. It
will have 5 parameters which can be varied.

The purpose of this is to test whether, when weighting random
points via the density, running an mcmc using the correlation
function of mock vs weighted randoms will converge to the
correct parameter values. For the actual 2 disk model, I have
so far not found this to be the case.

Therefore, I will generate stars with the same number as the
SEGUE data in each line of sight. I will then use jackknife
errors to run an mcmc in order to see if I converge to the
correct values.
