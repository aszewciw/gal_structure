"""
Takes the raw data file produced by Schlesinger et. all from SEGUE data
and selects only stars that qualify as gdwarfs. This sample is then
"""
import sys
import numpy as np
import math
import matplotlib.pyplot as plt
#sys.path.insert(0, '/Users/Adam/Python_files/SEGUE/first_attempts')

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


def calc_ave(x_min, x_max, y_min, y_max, x_var, y_var, weight_var, index_list):
    N_stars = 0
    weight_sum = 0
    weight_ave = 0

    for i in index_list:
        if x_var[i] > x_min and x_var[i] < x_max and y_var[i] > y_min and y_var[i] < y_max:
            # weight_sum += weight[i]
            weight_sum += weight_var[i]
            # weight_sum += type_weight[i]
            N_stars += 1

    if N_stars != 0:
        weight_ave = weight_sum / N_stars

    return(weight_ave)


array_side = 64
ends = 4
size = 2 * ends / array_side

type_ave = np.zeros((array_side, array_side))
rmag_ave = np.zeros((array_side, array_side))
combo_ave = np.zeros((array_side, array_side))

side = np.linspace(-1*ends, ends - size, array_side)


type_list = []
rmag_list = []
combo_list = []

for i in range(len(dist)):
    if dist[i] > 0 and dist[i] < ends:
        if weight[i] != 0 and weight[i] < 20:
            combo_list.append(i)
        if r_mag_weight[i] < 50 and r_mag_weight[i] != 0:
            rmag_list.append(i)
        if type_weight[i] < 2 and type_weight[i] != 0:
            type_list.append(i)

print(len(combo_list), len(rmag_list), len(type_list))


for i in range(len(type_ave)):
    y_min = side[i]
    y_max = side[i] + size

    for j in range(len(side)):
        x_min = side[j]
        x_max = side[j] + size
        type_ave[i, j] = calc_ave(x_min, x_max, y_min, y_max, x, z, type_weight, type_list)
        rmag_ave[i, j] = calc_ave(x_min, x_max, y_min, y_max, x, z, r_mag_weight, rmag_list)
        combo_ave[i, j] = calc_ave(x_min, x_max, y_min, y_max, x, z, weight, combo_list)




fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')
plt.title('test')
labels = ['-4', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '-3', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '-2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '-1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '0', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '3', ' ', ' ', ' ', ' ', ' ', ' ', ' 4']

# ax1 = fig.add_subplot( 221, axisbg='white', aspect='equal' )
# ax1.pcolor(combo_ave,cmap=plt.cm.Reds,edgecolors='r')
# ax1.set_xlim( 0, array_side )
# ax1.set_ylim( 0, array_side )
# ax1.set_xlabel( 'kpc toward galactic center --->')
# ax1.set_ylabel( 'z (kpc)' )
# plt.xticks(np.arange(0,array_side),labels)
# plt.yticks(np.arange(0,array_side),labels)
# ax1.set_title( 'Combines weights ')
# ax1.grid(b=False, which='majorminor')
# plt.grid(False, which="majorminor")


# plt.axis([0, array_side, 0, array_side])
# plt.xlabel('kpc toward galactic center --->')
# plt.ylabel('z (kpc)')
# plt.title('Combined weights')
# plt.xticks(np.arange(0,array_side),labels)
# plt.yticks(np.arange(0,array_side),labels)
# plt.grid(False, which="majorminor")



plt.subplot(221, aspect='equal')
plt.pcolor(combo_ave,cmap=plt.cm.Reds,edgecolors='r')
plt.axis([0, array_side, 0, array_side])
plt.xlabel('kpc toward galactic center --->')
plt.ylabel('z (kpc)')
plt.title('Combined weights')
plt.xticks(np.arange(0,array_side),labels)
plt.yticks(np.arange(0,array_side),labels)
# plt.grid(False, which="majorminor")

plt.subplot(222, aspect='equal')
plt.pcolor(rmag_ave,cmap=plt.cm.Reds,edgecolors='r')
plt.axis([0, array_side, 0, array_side])
# plt.xlabel('x (kpc)   Toward Galactic Center --->')
# plt.ylabel('z (kpc)')
plt.title('r_mag weights')
plt.xticks(np.arange(0,array_side),labels)
plt.yticks(np.arange(0,array_side),labels)

plt.subplot(224, aspect='equal')
plt.pcolor(type_ave,cmap=plt.cm.Reds,edgecolors='r')
plt.axis([0, array_side, 0, array_side])
# plt.xlabel('x (kpc)   Toward Galactic Center --->')
# plt.ylabel('z (kpc)')
plt.title('type weights')
plt.xticks(np.arange(0,array_side),labels)
plt.yticks(np.arange(0,array_side),labels)
plt.gca().grid(False)

plt.show()
    # # plt.show()

    # zmag = np.fabs(z)
    # print(min(zmag), max(zmag))