#!/usr/bin/env python

import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.colors as col

input_filename = '../data/chi2_los.dat'
input_file = open(input_filename, 'r')
pid, chi2_los = np.loadtxt(input_file, unpack=True)
input_file.close()

input_filename = '../data/todo_list.ascii.dat'
input_file = open(input_filename, 'r')
print input_file.readline()
pid2, pra, pdec, pl, pb = np.loadtxt(input_file, usecols=(0,1,2,5,6), unpack=True)
input_file.close()

pl = np.degrees(pl)
pb = np.degrees(pb)

Np = len(pid)

if len(pid) != len(pid2):
    sys.stderr.write("Error: Column mismatch.\n")
    sys.exit()

for i in range(Np):
    if pid[i] != pid2[i]:
        sys.stderr.write("Error: Column mismatch.\n")
        sys.exit()


gra, gdec = np.loadtxt('galplane_eq.dat', unpack=True)
gra = np.degrees(gra)
gdec = np.degrees(gdec)


plt.figure(figsize=(12,6), dpi=150)
plt.xlabel(r'RA')
plt.ylabel(r'Dec')
plt.xlim(0,360)
plt.ylim(-40,90)

plt.scatter(pra, pdec, c=chi2_los, faceted=False, s=20, cmap=cm.jet)
plt.plot(gra, gdec)

plt.colorbar()

plt.savefig('../plots/chi2_map.png')


plt.figure(figsize=(12,6), dpi=150)
plt.xlabel(r'l')
plt.ylabel(r'b')
plt.xlim(0,360)
plt.ylim(-90,90)

plt.scatter(pl, pb, c=chi2_los, faceted=False, s=20, cmap=cm.jet)
plt.axhline(0, linestyle='--', c='0.75')

plt.colorbar()

plt.show()
plt.savefig('../plots/chi2_map_galactic.png')

plt.figure(figsize=(12,6), dpi=150)
plt.xlabel(r'l')
plt.ylabel(r'b')
plt.xlim(0,360)
plt.ylim(-90,90)

plt.scatter(pl, pb, c=chi2_los, faceted=False, s=20, cmap=cm.rainbow)
plt.axhline(0, linestyle='--', c='0.75')

plt.colorbar()

plt.show()
plt.savefig('../plots/chi2_map_galactic_2.png')

plt.figure(figsize=(12,6), dpi=150)
plt.xlabel(r'l')
plt.ylabel(r'b')
plt.xlim(0,360)
plt.ylim(-90,90)

plt.scatter(pl, pb, c=chi2_los, faceted=False, s=20, cmap=cm.Spectral)
plt.axhline(0, linestyle='--', c='0.75')

plt.colorbar()

plt.show()
plt.savefig('../plots/chi2_map_galactic_3.png')


plt.figure(figsize=(12,6), dpi=150)
plt.xlabel(r'l')
plt.ylabel(r'b')
plt.xlim(0,360)
plt.ylim(-90,90)

cdict = {'red': ((0.0, 0.0, 0.0),
                 (0.5, 0.0, 0.0),
                 (1.0, 1.0, 1.0)),
         'green': ((0.0, 0.0, 0.0),
                   (0.5, 0.8, 0.8), 
                   (1.0, 0.0, 0.0)),
         'blue': ((0.0, 1.0, 1.0),
                  (0.5, 0.0, 0.0), 
                  (1.0, 0.0, 0.0))}
cmap1 = col.LinearSegmentedColormap('own1',cdict,N=256,gamma=0.75)
cmap2 = col.LinearSegmentedColormap.from_list('own2',['#0000ff', '#00ff00', '#ff0000'])

plt.scatter(pl, pb, c=chi2_los, faceted=False, s=80, cmap=cmap1)
plt.axhline(0, linestyle='--', c='0.75')

plt.colorbar()

plt.show()
plt.savefig('../plots/chi2_map_galactic_4.png')

