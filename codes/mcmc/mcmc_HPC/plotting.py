import numpy as np
import matplotlib.pyplot as plt

# Plots for MPI Implementation

N_procs = np.array([1, 2, 4, 8, 16, 32])
t_mpi = np.array([1494, 809, 496, 292, 189, 158])

# Serial times
t_icc = 1509
t_python = 7983

speedup = t_icc / t_mpi
eff = speedup / N_procs

speedup_py = t_python / t_mpi
plt.clf()

plt.figure(1)
plt.plot(N_procs, speedup, 'b')
plt.xlabel('Number of Processes')
plt.ylabel('Speedup')
plt.title('Speedup of MPI MCMC')
plt.savefig('speedup.png')


plt.figure(2)
plt.plot(N_procs, eff, 'b')
plt.xlabel('Number of Processes')
plt.ylabel('Efficiency (speedup/nprocs)')
plt.title('Efficiency of MPI MCMC')
plt.savefig('efficiency.png')

plt.figure(3)
plt.plot(N_procs, speedup_py, 'b')
plt.xlabel('Number of Processes')
plt.ylabel('Speedup')
plt.title('Speedup compared to Python version')
plt.savefig('python_speedup.png')

plt.clf()