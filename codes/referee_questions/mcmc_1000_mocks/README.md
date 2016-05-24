Testing of proper way to use errors for mcmc.

Here I will make 1000 mocks and run pair counting on all of them.
The standard deviation resulting from this pair counting will be
used in the mcmc instead of the jackknife errors.

My intention for now is to not include any "error" on the random
pair counting, but instead to only use the standard deviation
produced as described above.
