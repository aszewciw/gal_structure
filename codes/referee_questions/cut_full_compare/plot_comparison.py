import matplotlib.pyplot as plt
import numpy as np

filename = 'w_mean_1.dat'
w_mean_1 = np.genfromtxt(filename)

filename = 'w_mean_2.dat'
w_mean_2 = np.genfromtxt(filename)

filename = 'std_mean.dat'
std_mean = np.genfromtxt(filename)

y_range = 0.1
y_mid = 1
y_min = y_mid - y_range
y_max = y_mid + y_range

plt.clf()
plt.figure(1)

bins = np.arange(len(w_mean_2)) + 1
line_1 = np.ones(len(bins))

plt.title('Correlation comparison weighted mean')
plt.xlabel('Bin number')
plt.ylabel(r'$\displaystyle\frac{\xi_{cut}}{\xi_{full}}$')
plt.plot(bins, line_1, 'k')
plt.errorbar(bins, w_mean_1, yerr=std_mean, color='b', ecolor='b',
    elinewidth = 1.5, capthick = 1.5, capsize = 7)
plt.axis([0,13,y_min,y_max])
plt.savefig('corr_comp_weighted1.png')

plt.figure(2)
plt.title('Correlation comparison weighted mean (squared)')
plt.xlabel('Bin number')
plt.ylabel(r'$\displaystyle\frac{\xi_{cut}}{\xi_{full}}$')
plt.plot(bins, line_1, 'k')
plt.errorbar(bins, w_mean_2, yerr=std_mean, color='r', ecolor='r',
    elinewidth = 1.5, capthick = 1.5, capsize = 7)
plt.axis([0,13,y_min,y_max])
plt.savefig('corr_comp_weighted2.png')

plt.show()
plt.clf()
