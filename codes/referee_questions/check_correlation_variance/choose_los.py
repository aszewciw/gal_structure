'''
Choose 8 SEGUE l.o.s. in fairly different directions in the solar neighborhood.
Selection will be based on plate center's cartesian coordinates.
'''

from config import *
# import matplotlib.pyplot as plt

data_dir = './data/'

def main():

    # load pointing list
    input_filename = data_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file     = open(input_filename, 'rb')
    todo_list      = pickle.load(input_file)
    input_file.close()

    x1=[]
    x2=[]
    x3=[]
    x4=[]
    x5=[]
    x6=[]
    x7=[]
    x8=[]

    # plt.figure()


    for p in todo_list:

        x = p.cartesian_x
        y = p.cartesian_y
        z = p.cartesian_z

        # assign to appropriate octant
        if x>0 and y>0 and z>=0:
            x1.append(p)
            # plt.plot(x, y, 'ro')
            continue
        if x>0 and y>0 and z<0:
            x2.append(p)
            # plt.plot(x, y, 'ro')
            continue
        if x>0 and y<0 and z>=0:
            x3.append(p)
            # plt.plot(x, y, 'go')
            continue
        if x>0 and y<0 and z<0:
            x4.append(p)
            # plt.plot(x, y, 'go')
            continue
        if x<0 and y>0 and z>=0:
            x5.append(p)
            # plt.plot(x, y, 'ko')
            continue
        if x<0 and y>0 and z<0:
            x6.append(p)
            # plt.plot(x, y, 'ko')
            continue
        if x<0 and y<0 and z>=0:
            x7.append(p)
            # plt.plot(x, y, 'bo')
            continue
        if x<0 and y<0 and z<0:
            x8.append(p)
            # plt.plot(x, y, 'bo')
            continue

    index = 0
    master_list=[]

    master_list.append(x1[index])
    master_list.append(x2[index])
    master_list.append(x3[index])
    master_list.append(x4[index])
    master_list.append(x5[index])
    master_list.append(x6[index])
    master_list.append(x7[index])
    master_list.append(x8[index])

    # pickle output
    output_filename = data_dir + 'corr_list.dat'
    output_file     = open(output_filename, "wb")
    pickle.dump(master_list, output_file)
    output_file.close()

    output_file = data_dir + 'corr_list.ascii.dat'
    with open(output_file, 'w') as f:
        f.write(str(len(master_list)))
        f.write('\n')
        for p in master_list:
            f.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'
                .format(p.ID, p.ra_deg, p.dec_deg, p.ra_rad, p.dec_rad,
                    p.galactic_l_rad, p.galactic_b_rad,
                    p.cartesian_x, p.cartesian_y, p.cartesian_z,
                    p.N_star))

if __name__ == '__main__':
    main()