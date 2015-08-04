"""
Takes the raw data file produced by Schlesinger et. all from SEGUE data
and selects only stars that qualify as gdwarfs. This sample is then (decide as I go)
"""
import sys
import numpy as np
import pickle
#sys.path.insert(0, '/Users/Adam/Python_files/SEGUE/first_attempts')

data_path = '/Users/Adam/Python_files/SEGUE/first_attempts/'

class gdwarf(np.ndarray): pass

# def main():

    #Load all quantities in which we're interested for every single SEGUE star
r0, g0, dist, ra, dec, l, b, r_mag_weight, type_weight = np.loadtxt(data_path + 'raw_data.dat', unpack=True, usecols=[5, 6, 9, 17, 18, 20, 21, 34, 35])
    #np.savez('testing2.npz', r0=r0, g0=g0)


gdwarf.r0 = r0
gdwarf.g0 = g0

t = [gdwarf]

# gdwarf.x = np.cos(gdwarf.r0)

# print(gdwarf.r0[1], gdwarf.g0[1])

with open('newtest.txt', 'wb') as newfile:
    pickle.dump(gdwarf, newfile)





    # #Store index of each g_dwarf in a list
    # index_list = []

    # for i in range(len(r0)):
    #     if (dist[i] > 0 and (g0[i] - r0[i]) > 0.48 and (g0[i] - r0[i]) < 0.55 and r0[i] > 15.0  and r0[i] < 19.0):
    #         index_list.append(i)

    # #Save all quantities in a new numpy array
    # gdwarf_data = np.zeros((len(index_list), 9))

    # i = 0
    # j = 0
    # while i < len(gdwarf_data):
    #     gdwarf_data[i




# if __name__ == '__main__':
#     main()