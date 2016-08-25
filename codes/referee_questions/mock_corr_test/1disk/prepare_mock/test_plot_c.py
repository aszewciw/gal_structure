import numpy as np
import matplotlib.pyplot as plt

thin_file = './data/mocktest_thin.dat'
thin_Z, thin_R, thin_x, thin_y, thin_z = np.genfromtxt(thin_file, unpack=True)

thick_file = './data/mocktest_thick.dat'
thick_Z, thick_R, thick_x, thick_y, thick_z = np.genfromtxt(thick_file, unpack=True)


dist1 = thin_x * thin_x + thin_y * thin_y + thin_z * thin_z
dist2 = thick_x * thick_x + thick_y * thick_y + thick_z * thick_z
print(min(dist1), max(dist1))
print(min(dist2), max(dist2))
# plt.clf()
# fig = plt.figure(1)
# ax = fig.add_subplot(211, aspect='equal')
# plt.figure(1)
# plt.subplot(121, aspect='equal')
# plt.scatter(thick_R, thick_Z, c='red', s=3)
# plt.scatter(thin_R, thin_Z, c='blue', s=3)
# # plt.scatter(thick_R, thick_Z, c='red', s=3)
# plt.xlabel('Radius R (kpc)')
# plt.ylabel('Height Z (kpc)')
# plt.title('Mock Galaxy in Galaxy Centered Coordinates')
# plt.axis([5, 11, -3, 3])

# plt.subplot(122, aspect='equal')
# # plt.scatter(thin_x, thin_y, c='blue', s=3)
# plt.scatter(thick_x, thick_y, c='red', s=3)
# plt.scatter(thin_x, thin_y, c='blue', s=3)
# plt.xlabel('Equatorial x (kpc)')
# plt.ylabel('Equatorial y (kpc)')
# plt.title('Sun-Centered Cartesian Coordinates')
# plt.axis([-11, -5, -5, 5])

# z_min = -3.0
# z_max = 3.0
# step = 0.1
# bins = np.arange(z_min, z_max+step, step)

# r_min = 5.0
# r_max = 11.0
# step = 0.2
# bins = np.arange(r_min, r_max+step, step)

# plt.figure(1)
# plt.hist(r_thin, bins, color='blue')

# plt.savefig('Gal_center_mock.png')

# plt.figure(2)
# plt.subplot(121, aspect='equal')
# plt.scatter(x_thin, z_thin, c='blue', s=3)
# plt.scatter(x_thick, z_thick, c='red', s=3)
# plt.xlabel('x (kpc)')
# plt.ylabel('z (kpc)')
# plt.title('Mock Galaxy in Sun Centered Coordinates')
# plt.axis([-4, 4, -5, 5])

# plt.subplot(122, aspect='equal')
# plt.scatter(x_thin, y_thin, c='blue', s=3)
# plt.scatter(x_thick, y_thick, c='red', s=3)
# plt.xlabel('x (kpc)')
# plt.ylabel('y (kpc)')
# plt.title('Mock Galaxy Overhead view')
# plt.axis([-4, 4, -5, 5])

# plt.savefig('Sun_center_mock.png')

# plt.figure(3)
# plt.scatter(np.degrees(ra_thin), np.degrees(dec_thin), c='blue', s=3)
# plt.scatter(np.degrees(ra_thick), np.degrees(dec_thick), c='red', s=3)
# plt.xlabel('ra (degrees)')
# plt.ylabel('dec (degrees)')
# plt.show()
# plt.clf()