import numpy as np

N_mock = 133
N_jackknife = 10

remain = N_mock % N_jackknife

for i in range( N_jackknife ):

    slice_length = int( N_mock / N_jackknife )
    lower_ind = i * slice_length
    if i < remain:
        lower_ind += i
        slice_length += 1
    else:
        lower_ind += remain

    upper_ind = lower_ind + slice_length

    remove_me = np.arange(lower_ind, upper_ind, 1)

    print(remove_me)