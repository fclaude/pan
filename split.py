#!/usr/bin/python

import sys
import shutil
import random
import data

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print "usage: %s <file list> <training dir> <testing dir> <percentage training>" % (sys.argv[0])
        sys.exit(0)

    ages = [18, 25, 35, 50, 65]
    genders = ["MALE", "FEMALE"]
    results = {}
    sets = {}
    shutil.copyfile(sys.argv[1] + "/truth.txt", sys.argv[3] + "/truth.txt")
    shutil.copyfile(sys.argv[1] + "/truth.txt", sys.argv[2] + "/truth.txt")
    fp = open(sys.argv[1] + "/truth.txt")
    for l in fp.readlines():
        datar = l[:-1].split(":::")
        results[datar[0]] = (data.AgeStringToInt(datar[2]),datar[1])
        sets[(results[datar[0]])] = datar[0]

    percentage = int(sys.argv[4])
    for v in results.keys():
        if random.randint(0,100) > percentage:
            #add to testing
            path=sys.argv[1] + "/" + v + ".xml"
            shutil.copyfile(path, sys.argv[3] + "/" + v + ".xml")
        else:
            #add to training
            path=sys.argv[1] + "/" + v + ".xml"
            shutil.copyfile(path, sys.argv[2] + "/" + v + ".xml")
