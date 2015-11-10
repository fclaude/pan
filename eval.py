#!/usr/bin/python

import sys
from data import ReadMeta, GENDERS, AGES
import util_functions
import warnings

# Evaluates a classifier using the common API
if __name__ == "__main__":
    warnings.simplefilter("ignore")
    if len(sys.argv) != 3:
        print "usage: %s <basename> <test basename>" % (sys.argv[0])
        sys.exit(0)

    basename = sys.argv[1]
    test_basename = sys.argv[2]
    meta = ReadMeta(test_basename)
    classifier = util_functions.LoadClassifier(basename)

    total_tests = 0
    age_correct = 0
    gender_correct = 0
    all_correct = 0

    confusion_matrix = {}

    for i in xrange(len(meta.ids)):
        age = meta.GetAge(i)
        gender = meta.GetGender(i)
        docs = []
        for j in xrange(meta.GetNumDocuments(i)):
            docs.append(meta.GetDocument(i, j))
        age_pred = classifier.GuessAge(docs)
        gender_pred = classifier.GuessGender(docs)
        p_pred = classifier.Guess(docs)
        if age_pred == age: age_correct += 1
        if gender_pred == gender: gender_correct += 1
        if (gender, age) == p_pred: all_correct += 1
        if not confusion_matrix.has_key((gender, age)):
            confusion_matrix[(gender, age)] = {}
        confusion_matrix[(gender, age)][p_pred] = confusion_matrix[(gender, age)].get(p_pred, 0) + 1
        total_tests += 1
    
    print "Total guessed        : ", all_correct, ":", 100. * all_correct / total_tests,""
    print "Total guessed age    : ", age_correct, ":", 100. * age_correct / total_tests,""
    print "Total guessed gender : ", gender_correct, ":", 100. * gender_correct / total_tests,""

    for gender in GENDERS:
        for age in AGES:
            if confusion_matrix.has_key((gender, age)):
                print "(", gender,", ", age,") => ",
                for gender2 in GENDERS:
                    for age2 in AGES:
                        if confusion_matrix[(gender, age)].has_key((gender2, age2)):
                            print "(", gender2,", ", age2,", ",confusion_matrix[(gender, age)].get((gender2, age2),0),") ",
                print ""