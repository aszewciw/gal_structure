import numpy as np
from config import *
import matplotlib.pyplot as plt

# # def main():

# filename = str(input('Enter filename with .npz extension: '))
filename = 'data/victor_test.npz'

with np.load(filename) as d:
    a         = d['A']
    eff       = d['EFF']
    chi2      = d['CHI2']
    z_thick   = d['Z_THICK']
    z_thin    = d['Z_THIN']
    r_thick   = d['R_THICK']
    r_thin    = d['R_THIN']
    chi2_test = d['CHI2_TEST']


filename = 'data/victor_test_pt2.npz'

with np.load(filename) as d:
    a = np.append(a, d['A'])
    eff       = np.append(eff, d['EFF'])
    chi2      = np.append(chi2, d['CHI2'])
    z_thick   = np.append(z_thick, d['Z_THICK'])
    z_thin    = np.append(z_thin, d['Z_THIN'])
    r_thick   = np.append(r_thick, d['R_THICK'])
    r_thin    = np.append(r_thin, d['R_THIN'])
    chi2_test = np.append(chi2_test, d['CHI2_TEST'])


loop = np.arange(len(a))

# Delete first N elements of numpy array
frac_deleted = 0.05
num_deleted  = frac_deleted * len(a)
index_delete = np.arange(num_deleted)
chi2         = np.delete(chi2, index_delete)
z_thick      = np.delete(z_thick, index_delete)
z_thin       = np.delete(z_thin, index_delete)
r_thick      = np.delete(r_thick, index_delete)
r_thin       = np.delete(r_thin, index_delete)
a            = np.delete(a, index_delete)
loop = np.delete(loop, index_delete)

plt.clf()


plt.figure(1)
plt.subplot(211)
plt.xlabel("Thin Disk Scale Height")
plt.ylabel("Thick Disk Scale Height")
plt.scatter(z_thin, z_thick, c=chi2, s=3)
plt.colorbar()

plt.subplot(212)
plt.xlabel("Thin Disk Scale Length")
plt.ylabel("Thick Disk Scale Length")
plt.scatter(r_thin, r_thick, c=chi2, s=3)
plt.colorbar()
# plt.savefig('Scales_Feb11.png')


# x = [0, 50000, 100000, 150000]

plt.figure(2)
plt.subplot(321)
# plt.xlabel("Loop Number")
# plt.xticks(x)
plt.ylabel("Thin Scale Height")
plt.scatter(loop, z_thin, c=chi2, s=2)
# plt.axis([0, len(loop), min(z_thin), max(z_thin)])

plt.subplot(322)
# plt.xlabel("Loop Number")
# plt.xticks(x)
plt.ylabel("Thick Scale Height")
plt.scatter(loop, z_thick, c=chi2, s=2)
# plt.axis([0, len(loop), min(z_thick), max(z_thick)])

plt.subplot(323)
# plt.xlabel("Loop Number")
# plt.xticks(x)
plt.ylabel("Thin Scale Length")
plt.scatter(loop, r_thin, c=chi2, s=2)
# plt.axis([0, len(loop), min(r_thin), max(r_thin)])

plt.subplot(324)
plt.xlabel("Loop Number")
# plt.xticks(x)
plt.ylabel("Thick Scale Length")
plt.scatter(loop, r_thick, c=chi2, s=2)
# plt.axis([0, len(loop), min(r_thick), max(r_thick)])

plt.subplot(325)
plt.xlabel("Loop Number")
# plt.xticks(x)
plt.ylabel("Thick:thin ratio")
plt.scatter(loop, a, c=chi2, s=2)
# plt.axis([0, len(loop), min(a), max(a)])
plt.colorbar()
# plt.savefig("loops_chi2_Feb11.png")

plt.show()
plt.clf()