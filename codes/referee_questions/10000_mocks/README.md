# 10000 mocks using the "fiducial" parameters:
* Parameters are
    * z0_thin = 0.233
    * z0_thick = 0.674
    * r0_thin = 2.34
    * r0_thick = 2.51
    * n_thick/n_thin = 0.1

* Folders included:
    * prepare_mocks - makes 10000 mocks from fiducial parameters
        * One mock is made per each SEGUE l.o.s.
    * errors_pairs - counts pairs in different radial bins
        * Stupidly, the bins are not made here. See the config file for their dir
    * density_errors - an alternative to the pair counting; compute density in shells of spherical coordinates
        * This is primarily used in testing the correctness of my mocks and whether the pair counting method works.