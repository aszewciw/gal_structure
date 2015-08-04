#!/usr/bin/env python

from collections import defaultdict

from config import *

def main():


    # load the todo pointing list
    input_filename = data_dir + 'todo_list.dat'
    sys.stderr.write('Loading from file {} ...\n'.format(input_filename))
    input_file = open(input_filename, 'r')
    todo_list = pickle.load(input_file)
    input_file.close()

    # calculate the average, standard deviation, and error
    cor = defaultdict(list)

    # calculate correlation function for each plate
    for p in todo_list:

        cor_file = data_dir + 'correlation_' + p.ID + '.dat'

        if not os.path.isfile(cor_file):
            sys.stderr.write('Warning: ' + cor_file + ' does not exist.\n')
            continue
        if os.path.getsize(cor_file) == 0:
            sys.stderr.write('Warning: ' + cor_file + ' is empty.\n')
            continue

        # read in correlations of each plate
        for line in file(cor_file):
            if line.lstrip().startswith('#'):
                continue
            index = float(line.split()[0])
            x = line.split()[1]
            x = 0.0 if x == 'inf' or x == 'nan' else float(x)
            # each dictionary item has a list of correlations
            cor[index].append(x)

    # take average
    out = defaultdict(list)

    for k in cor:

        n, mean, std, err = len(cor[k]), 0, 0, 0
        mean = float(sum(cor[k])) / n

        for i in cor[k]:
            std += (i - mean) * (i - mean)

        std = math.sqrt(std / (n - 1))
        err = std / math.sqrt(n)

        out[k] = [mean, std, err]

    # output
    output_filename = data_dir + 'correlation.dat'
    output_file = open(output_filename, 'w')

    for k in sorted(out.iterkeys()):

        output_file.write("{0}\t{1}\t{2}\t{3}\n"
                          .format(str(k), str(out[k][0]), str(out[k][1]), str(out[k][2])))

    output_file.close()
    sys.stderr.write('Results output to {} . \n'.format(output_filename))

if __name__ == '__main__' :
    main()