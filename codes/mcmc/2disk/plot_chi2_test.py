from config import *
import matplotlib.pyplot as plt

# def main():

# filename = str(input('Enter filename with .npz extension: '))
filename = 'new_chi2_check.npz'
# filename = out_dir + filename

with np.load(filename) as d:
    chi2  = d['CHI2']
    los   = d['LOS']
    MM    = d['MM']
    DD_MM = d['DDMM']
    sig2  = d['SIG2']

print('Chi squared is ', np.sum(chi2))

# print(len(chi2), len(los), len(MM), len(DD_MM), len(sig2))

for i in range(len(chi2)):
    if chi2[i] >1000:
        print(los[i], MM[i], DD_MM[i], sig2[i], chi2[i])

# print(count)
plt.figure(1)
plt.subplot(211)
plt.xlabel('los')
plt.ylabel('chi2')
plt.scatter(los, chi2, s=1)


plt.subplot(212)
plt.xlabel('los')
plt.ylabel('sig2')
plt.scatter(los, sig2, s=1)
# plt.savefig('mock_rk_rn.png')

plt.figure(2)
plt.subplot(211)
plt.xlabel('los')
plt.ylabel('MM')
plt.scatter(los, MM, s=1)

plt.subplot(212)
plt.xlabel('los')
plt.ylabel('DD/MM')
plt.scatter(los, DD_MM, s=1)
# plt.savefig('mock_zk_zn.png')

plt.show()
