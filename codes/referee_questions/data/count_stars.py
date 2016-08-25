import numpy as np

ID, N_stars = np.genfromtxt('todo_list.ascii.dat', usecols=[0, 10], unpack=True, skip_header=1)

stars_total = np.sum(N_stars)

for i in range(len(ID)):
    if N_stars[i]<50:
        print(ID[i], N_stars[i])