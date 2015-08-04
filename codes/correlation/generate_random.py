#!/usr/bin/env python

from config import *

#------------------------------------------------------------------------------
def random_unit(Ntot, pointing):
    """
    Generate random points for a given pointing in the sky.

    Keywords arguments:
    Ntot  -- Total number of random points needed.
    pointing -- A Pointing instance.

    Return a list of random points.
    Each element in the list is a Point instance, which should contain
    RA, Dec, distance, x, y, z, etc.
    """

    plate_size_cos = math.cos(PLATE_RADIUS_RADIANS) # the cos of the plate size

    center = (pointing.cartesian_x, pointing.cartesian_y, pointing.cartesian_z)

    random_sample = []

    while len(random_sample) < Ntot :

        aRandom = Point() # create a random point as a Point instance

        # generate a random number on [0,1]
        u = random.random()
        v = random.random()

        # Draw a random angular radius from the center for uniform distribution on a cap
        phi = math.acos(1 - u * (1 - plate_size_cos))

        # raise a vector from the center vector in Dec direction and get Cartesian coords
        ra = pointing.ra_rad
        dec = pointing.dec_rad + phi

        vec = eq2cart(ra, dec, 1.0)

        # rotate the vector a random angle around the center axis vector,
        # using Rodrigues' formula

        theta = v * 2.0 * math.pi

        vec_rotated = rodrigues(center, vec, theta)

        eq = cart2eq(vec_rotated[0], vec_rotated[1], vec_rotated[2])

        aRandom.cartesian_x = vec_rotated[0]
        aRandom.cartesian_y = vec_rotated[1]
        aRandom.cartesian_z = vec_rotated[2]

        aRandom.ra_rad = eq[0]
        aRandom.dec_rad = eq[1]
        aRandom.distance = eq[2]

        aRandom.ra_deg = math.degrees(aRandom.ra_rad)
        aRandom.dec_deg = math.degrees(aRandom.dec_rad)

        #quickly check distance, should be 1
        if math.fabs(aRandom.distance - 1) > 1.0e-5:
            sys.stderr.write("Error: rotated vector is not unit!\n")

        #using dot product to check
        if dot(vec_rotated, center) < plate_size_cos:
            sys.stderr.write("Warning: there is certainly something wrong..\n")
            sys.stderr.write("dot = {0}\t cos = {1}\n"
                             .format(dot(cart, center), plate_size_cos))

        # append the generated random point to the list
        random_sample.append(aRandom)

    return random_sample
#-------------------------------------------------------------------------
# def assign_distance(random_sample, star_list):

#     # assign each star's distance to couple of random points
#     for n in range(len(random_sample)):
#         random_sample[n].distance = star_list[n % len(star_list)].distance
#         random_sample[n].weight = star_list[n % len(star_list)].weight

#     # recalculate the x, y, z of random points based on the assigned distance.
#     for p in random_sample:
#         p.cartesian_x, p.cartesian_y, p.cartesian_z = eq2cart(p.ra, p.dec, p.distance)

#     return random_sample

#--------------------------------------------------------------------------
def assign_distance(random_sample, r1, r2):
    """
    Assign distances to random points.
    Random points are distributed uniformly in a shell between [rmin, rmax].
    """

    #
    if r2 <= r1:
        sys.stderr.write("Error: Cannot assign distance. "
                         "Shell parameters error.\n"
                         "The max radius smaller than the min.\n ")
        sys.exit()

    a = r1 ** 3
    b = r2 ** 3 - a

    for p in random_sample:

        u = random.random()

        p.distance = (u * b + a) ** (1.0 / 3.0)

    # recalculate the x, y, z of random points based on the assigned distance.
    for p in random_sample:
        p.cartesian_x, p.cartesian_y, p.cartesian_z = eq2cart(p.ra_rad, p.dec_rad, p.distance)

    return random_sample

#--------------------------------------------------------------------------

def main():

    # load the todo pointing list
    input_filename = data_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file = open(input_filename, 'r')
    todo_list = pickle.load(input_file)
    input_file.close()

    sys.stderr.write('Generating random samples..\n')
    sys.stderr.write('{} line-of-sight to generate..\n'.format(len(todo_list)))

    # generate random sample and star sample for individual plates
    for p in todo_list:

        # a progress indicator
        if todo_list.index(p) % (len(todo_list) / 10) == 0:
            sys.stderr.write('Generating #{} of {} ..\n'
                             .format(todo_list.index(p), len(todo_list)))

        if p.N_star == 0:
            sys.stderr.write('Error: Empty star list. \n')
            continue

        Ntot = p.N_star * 100 # total number of random points to generate

        # generate random numbers on a unit sphere
        random_sample = random_unit(Ntot, p)

        r1 = INNER_DISTANCE_LIMIT
        r2 = OUTER_DISTANCE_LIMIT

        # assign distance to random sample
        random_sample = assign_distance(random_sample, r1, r2)

        # set random points' weight to 1
        for i in random_sample:
            i.weight = 1.0

        # output
        output_filename = data_dir + 'random_' + p.ID + '.dat'
        output_file = open(output_filename, "w")
        pickle.dump(random_sample, output_file)
        output_file.close()

        # output ascii format
        output_filename = data_dir + 'random_' + p.ID + '.xyzw.dat'
        output_file = open(output_filename, "w")
        for i in random_sample:
            output_file.write('{}\t{}\t{}\t{}\n'
                              .format(i.cartesian_x, i.cartesian_y, i.cartesian_z,
                                      i.weight))
        output_file.close()


    sys.stderr.write('Done. Random samples output to {} .\n'.format(data_dir))

if __name__ == '__main__' :
    main()

