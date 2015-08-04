import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm

file_path = '/Users/Adam/Python_files/SEGUE/first_attempts/'

#Load all quantities in which we're interested for every single SEGUE star
r0, g0, dist, l, b, r_mag_weight, type_weight = np.loadtxt(file_path + 'raw_data.dat', unpack=True, usecols=[5, 6, 9, 20, 21, 34, 35])

#Convert to radians

l_rad = np.radians(l)
b_rad = np.radians(b)

#Create arrays for x, y, and z in galactic coordinates
x = dist * np.cos(l_rad) * np.cos(b_rad)
y = dist * np.sin(l_rad) * np.cos(b_rad)
z = dist * np.sin(b_rad)

weight = r_mag_weight * type_weight

x_plt = []
z_plt = []
weight_plt = []

for i in range(len(x)):
    if dist[i] > 0 and dist[i] < 5 and weight[i] < 20:
        x_plt.append(x[i])
        z_plt.append(z[i])
        weight_plt.append(weight[i])

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')
plt.scatter(x_plt, z_plt, s=5, c=weight_plt, cmap='Reds_r')
plt.show()