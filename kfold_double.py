#!/usr/bin/python
import sys
import shutil
import random
import data
import os
import math

def get_stats(x):
  n = 0
  S = 0.0
  m = 0.0
  for x_i in x:
    n = n + 1
    m_prev = m
    m = m + (x_i - m) / n
    S = S + (x_i - m) * (x_i - m_prev)
  return {'mean': m, 'variance': S/n}

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print "usage: %s <file list> <k> <classifier_gender> <classifier_age> " % (sys.argv[0])
        sys.exit(0)

    ages = [18, 25, 35, 50, 65]
    if not os.path.exists("k_training"):
        os.makedirs("k_training")
    else:
        shutil.rmtree("k_training")
        os.makedirs("k_training")


    if not os.path.exists("k_test"):
        os.makedirs("k_test")
    else:
        shutil.rmtree("k_test")
        os.makedirs("k_test")

    extension = ""
    classif = sys.argv[3]
    if classif == "EntropyClassifier": extension = ".entropy"
    if classif == "MTFClassifier": extension = ".mtf"
    if classif == "WordCountClassifier": extension = ".count"
    if classif == "CompressClassifier": extension = ".hvoc"
    if classif == "WordCountNormalizedClassifier": extension = ".ncount"


    extension2 = ""
    classif2 = sys.argv[4]
    if classif2 == "EntropyClassifier": extension2 = ".entropy"
    if classif2 == "MTFClassifier": extension2 = ".mtf"
    if classif2 == "WordCountClassifier": extension2 = ".count"
    if classif2 == "CompressClassifier": extension2 = ".hvoc"
    if classif2 == "WordCountNormalizedClassifier": extension2 = ".ncount"


    k = int(sys.argv[2])
    genders = ["MALE", "FEMALE"]
    results = {}
    shutil.copyfile(sys.argv[1] + "/truth.txt", "./k_training/truth.txt")
    shutil.copyfile(sys.argv[1] + "/truth.txt", "./k_test/truth.txt")
    fp = open(sys.argv[1] + "/truth.txt")
    for l in fp.readlines():
        datar = l[:-1].split(":::")
        results[datar[0]] = (data.AgeStringToInt(datar[2]),datar[1])

    if len(results)%k ==0:
	set_len = len(results)/k

    else:
	set_len = len(results)/k +1

    print "# Total Elements                        : " + str(len(results))
    print "# Amount of elements per test set   : " + str(set_len)
    print "# Amount of elements per training set       : " + str(len(results) - set_len)

    if set_len < 1:
        print "k is too big!"
        sys.exit(0)
    k_data = []
    k_list = []
    i = 0
    for v in results.keys():
        if i % set_len == 0  and len(k_list) > 0:
            k_data.append(k_list)
            k_list = []
        k_list.append(v)
        i+=1

    if(len(k_list)>0):
	k_data.append(k_list)

    pivot = 0
    stats = {}
    stats["total"] = []
    stats["age"] = []
    stats["gender"] = []

    for pivot in range (0,k):
        shutil.rmtree("k_training")
        os.makedirs("k_training")
        shutil.rmtree("k_test")
        os.makedirs("k_test")
        shutil.copyfile(sys.argv[1] + "/truth.txt", "./k_training/truth.txt")
        shutil.copyfile(sys.argv[1] + "/truth.txt", "./k_test/truth.txt")
        for i in range(0,len(k_data)):
            for v in k_data[i]:
                path=sys.argv[1] + "/" + v + ".xml"
                if i != pivot:
                    out_path= "./k_training/" + v + ".xml"
                else:
                    out_path="./k_test/"+ v + ".xml"
                shutil.copyfile(path, out_path)

        print "# evaluating pivot = " + str(pivot)
        output = os.popen('python parse.py ./k_training/ ./k_training/').read()
        print "# parsing of k_trainging done!"

        output = os.popen('python parse.py ./k_test/ ./k_test/').read()
        print "# parsing of k_test done!"

        start = time.time()
        output = os.popen('python train.py ' + classif + ' ./k_training/').read()
        end = time.time()
        print ("# training of " + classif + " done in %f seconds!" % (end-start))

        start = time.time()
        output = os.popen('python train.py ' + classif2 + ' ./k_training/').read()
        end = time.time()
        print "# training of " + classif2 + " done in %f seconds!" % (end-start))


        start = time.time()
        output = os.popen('python eval_double.py ./k_training/'+extension +' ./k_training/'+extension2 +" ./k_test/").read()
        field = 0
        lines = output.split("\n")
        for line in lines:
            line_data = line.split(":")
            #print line_data
            if len(line_data) == 3:
                if field == 3:
                    field = 0
                if field == 0:
                    stats["total"].append(float(line_data[2]))
                    print "total:\t" + line_data[2]+ " :\t " + line_data[1]
                if field == 1:
                    stats["age"].append(float(line_data[2]))
                    print "age:\t" + line_data[2] + " :\t " + line_data[1]

                if field == 2:
                    stats["gender"].append(float(line_data[2]))
                    print "gender:\t" + line_data[2]+ " :\t " + line_data[1]

                field+=1
        end = time.time()
        print "# evaluated in %f seconds" % (end-start)

    print "General Average : " + str(get_stats(stats["total"])["mean"])
    print "General Stdev : " + str(math.sqrt(get_stats(stats["total"])["variance"]))
    print "General Max : " + str(max(stats["total"]))
    print "General Min : " + str(min(stats["total"]))

    print "Age Average : " + str(get_stats(stats["age"])["mean"])
    print "Age Stdev : " + str(math.sqrt(get_stats(stats["age"])["variance"]))
    print "Age Max : " + str(max(stats["age"]))
    print "Age Min : " + str(min(stats["age"]))

    print "Gender Average : " + str(get_stats(stats["gender"])["mean"])
    print "Gender Stdev : " + str(math.sqrt(get_stats(stats["gender"])["variance"]))
    print "Gender Max : " + str(max(stats["gender"]))
    print "Gender Min : " + str(min(stats["gender"]))

        #print output

    # percentage = int(sys.argv[4])
    # for v in results.keys():
    #     if random.randint(0,100) > percentage:
    #         #add to testing
    #         path=sys.argv[1] + "/" + v + ".xml"
    #         shutil.copyfile(path, sys.argv[3] + "/" + v + ".xml")
    #     else:
    #         #add to training
    #         path=sys.argv[1] + "/" + v + ".xml"
    #         shutil.copyfile(path, sys.argv[2] + "/" + v + ".xml")
