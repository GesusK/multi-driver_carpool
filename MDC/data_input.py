__author__ = 'Arthur'
"""
This class is used to take different types of input data,
and out put a driver list, along with a passenger list.
Currently it will only support *.csv.
csv sample:
time,   name,   phone,  address,    isDriver,   comment
"""

import csv
from Member import Member

def read_from_csv(csv_file):
    dvr_list = list()
    psg_list = list()
    with open(csv_file) as file:
        reader = csv.DictReader(file, delimiter='|')
        for row in reader:
            tmp_name = row["name"] + " - " + row["phone"]
            if row["isDriver"].strip() == "yes":
                isD = True
            else:
                isD = False

            tmp_mem = Member(tmp_name, row["address"] + ", canada", isD)
            if isD:
                dvr_list.append(tmp_mem)
            else:
                psg_list.append(tmp_mem)

    return dvr_list, psg_list



if __name__ == '__main__':
    [dlist, plist] = read_from_csv("test.csv")
    print "End of test."


