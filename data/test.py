import os, sys, math
import string, csv
import pickle

def plate_csv(filename):
    """
    Read plates' information from csv file obtained from database using SQL.
    Return a list of plates' information. Each element in the list is a python
    dictionary of plate's information. Dictionary keys are from the header of
    the csv file, so it's the same as in the sdss database.

    For example, a plate's plateID can be called as plate[5]['plateID']
    """

    f = open(filename,'r')
    plates = []

    try:
        plist = csv.DictReader(f)
        for record in plist:
            plates.append(record)

    finally:
        f.close()

    return plates


plates = plate_csv('segue.plates.csv')

count = 0
plt = []
flag = 0
    # picking plates as needed
for i in plates:
    if ((i['survey'] == 'segue1' or i['survey'] == 'segue2') and (i['programName'] == 'segue' or i['programName'] == 'seguefaint' or i['programName'] == 'segue2') and (i['plateQuality'] == 'good')):
        plt.append([i['ra'], i['dec'], i['plate'], flag])
        count += 1

print(count)