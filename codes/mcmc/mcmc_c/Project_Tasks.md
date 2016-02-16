Modeling this code after Will French's. For now, I will
assume that the counts in DD have already been done.
I will also assume that all of the random points have
been pre-binned. Thus what I need to do is the following:
                                                                        Done?
    1.  Command line function call with number of mcmc loops    |
        and output file name...or maybe just the former. I      |       N
        could replace the output file name.                     |
                                                                |
    2.  Read in following files:                                |       N
        a. Bin info (min, max, number)                          |       N
        b. Pre-binned pair indices for randoms                  |       N
            num_files = num_los * num_bins                      |
        c. File with Z and R for randoms                        |
            num_files = num_los                                 |
        d. Normalized DD counts                                 |       N
            num_files = num_los each with                       |
        e.