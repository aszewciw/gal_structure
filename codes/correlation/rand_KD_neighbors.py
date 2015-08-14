import numpy as np
import math
from scipy import spatial
from config import *


bin_min = 0.001
bin_max = 2
N_bins = 26
bins = np.linspace(math.log(bin_min), math.log(bin_max), N_bins)
bins = np.exp(bins)
# print(bins)
# bins = bins ** 2

# total = 0
# pair_count = np.zeros(len(bins) - 1)

# xyz= np.genfromtxt('star_35.xyzw.dat', usecols = [0, 1, 2])
# weight= np.genfromtxt('star_35.xyzw.dat', usecols = [3])

# for i in range(len(xyz)):
#     for j in range(i + 1, len(xyz)):
#         dist_sq = np.sum((xyz[i] - xyz[j]) * (xyz[i] - xyz[j]))
#         N_stars = weight[i] * weight[j]
#         total += N_stars

#         for k in range(len(pair_count)):
#             if dist_sq > bins[k] and dist_sq <= bins[k + 1]:
#                 pair_count[k] += N_stars
#                 break

# print(sum(pair_count))
# print(pair_count/total)






def rand_pairs(xyz, tree, bins):
    Npairs = tree.count_neighbors(tree, bins)

    Npairs = Npairs - len(xyz)

    i = len(Npairs) - 1
    while i > 0:
        Npairs[i] -= Npairs[i - 1]
        i -= 1

    Npairs_adj = np.zeros(len(Npairs) - 1)
    for i in range(len(Npairs_adj)):
        Npairs_adj[i] = Npairs[i + 1]

    return Npairs_adj


rand_xyz = np.genfromtxt('random_161.xyzw.dat', usecols = [0, 1, 2])

rand_tree = spatial.KDTree(rand_xyz)

N_rand = rand_pairs(rand_xyz, rand_tree, bins)

#Below is what QQ uses for the normalization
points = 0
for i in range(len(rand_xyz)):
    points += i

N_rand = N_rand / points

np.savetxt('random_counts.txt', N_rand)

