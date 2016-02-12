from config import *
import matplotlib.pyplot as plt
import matplotlib

'''
A simple code to analyze the relative contributions
of the random and data jackknife errors.
'''

input_filename = rawdata_dir + 'todo_list.dat'
input_file     = open(input_filename, 'rb')
todo_list      = pickle.load(input_file)
input_file.close()
N_los          = len(todo_list)


binplt = np.zeros(Nbins)
for i in range(len(binplt)):
    binplt[i] = bins[i]

fig = plt.figure(figsize = (10, 8))
ax = fig.add_subplot(1,1,1, axisbg = 'white')
ax.set_xlabel('r (kpc)')
# ax.set_ylabel(r'$\displaystyle\frac{\delta_{DD} - \delta_{MM}}{\delta_{DD}}$')
ax.set_ylabel(r'$\displaystyle\frac{\frac{\delta_{MM}^2}{MM^2}}{\frac{\delta_{MM}^2}{MM^2} + \frac{\delta_{DD}^2}{DD^2}}$')
ax.set_title('Jackknife Error Comparison')
ax.set_xscale('log')
ax.set_xticklabels(['0.01', '0.1', '1'])
ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

ax.grid(True, color='k', linestyle = '--')

# make array for calculating total and mean
errors = np.zeros((len(todo_list), len(binplt)))
N_errs = np.zeros(len(binplt))

for j in range(len(todo_list)):

    p = todo_list[j]

    # Load jackknife errors as numpy arrays: one error for each bin
    uni_jk_file = jk_dir + 'uniform_' + p.ID + '_jk_error.dat'
    uni_jk_err  = np.genfromtxt(uni_jk_file, unpack=True, usecols=[7])
    dat_jk_file = jk_dir + 'star_' + p.ID + '_jk_error.dat'
    dat_jk_err  = np.genfromtxt(dat_jk_file, unpack=True, usecols=[7])
    err2_temp   = uni_jk_err ** 2 + dat_jk_err ** 2

    err_mm_2 = uni_jk_err ** 2
    frac = np.zeros(len(uni_jk_err))

    for i in range(len(uni_jk_err)):
        if dat_jk_err[i] != 0:
            frac[i] = err_mm_2[i] / err2_temp[i]
            errors[j, i] = frac[i]
            N_errs[i] += 1


    ax.plot(binplt, frac, '0.75', zorder = -42)
    plt.axis([0.005, 2, 0, 1])

mean = np.sum(errors, axis=0)
mean /= N_errs
var = (errors - mean) * (errors - mean)
var = np.sum(var, axis = 0) / N_errs
std = np.sqrt(var)
error = std / np.sqrt(N_errs)

ax.errorbar(binplt, mean, error, fmt = 'ro', ecolor = 'r', elinewidth = 1.5, capthick = 1.5, capsize = 7)

plt.show()