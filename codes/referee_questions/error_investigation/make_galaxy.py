'''
Generates an entire Milky Way based on a two-disk model.
Model may be over dense (100 billion stars).
We will only extend 3 kpc beyond position of the sun so
that we fill a volume which contains our segue lines of
sight under rotation

NOTE: Don't run this on local machine. Only on bender.

'''

# Set model parameters

def gal_weights(Z, R):
    '''
    Returns a weight based on a particular model of the MW.
    For now we will use a two-disk model with the form below.
    This can be expanded at a later time.

    Z - Height above/below galactic plane
    R - Distance from galactic center

    '''

    # Parameters
    thick_s_height = 0.674
    thick_s_length = 2.51
    thin_s_height = 0.233
    thin_s_length = 2.34
    a = 0.12                            #Taken from a paper (indicate which one)


    weight = ( ( ( math.cosh(Z / 2 / thin_s_height) ) ** (-2) )
        * math.exp(-R / thin_s_length) +
        a * ( ( math.cosh(Z / 2 / thick_s_height) ) ** (-2) )
        * math.exp(-R / thick_s_length))

    return weight