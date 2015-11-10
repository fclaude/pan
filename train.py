#!/usr/bin/python

import sys
import util_functions
from data import ReadMeta
import warnings

# Trains a classifier using the common API
if __name__ == "__main__":
    warnings.simplefilter("ignore")
    if len(sys.argv) != 3:
        print "usage: %s <classifier> <filename>" % (sys.argv[0])
        print "\n\tSupported classififers: WordCountClassifier, WordCountNormalizedClassifier"
        print "\t\tEntropyClassifier, CompressClassifier"
        sys.exit(0)

    classifier = sys.argv[1]
    basename = sys.argv[2]
    meta = ReadMeta(basename)
    classifier = util_functions.GetClassifier(classifier, basename)
    for i in xrange(len(meta.ids)):
        age = meta.GetAge(i)
        gender = meta.GetGender(i)
        docs = []
        for j in xrange(meta.GetNumDocuments(i)):
            docs.append(meta.GetDocument(i, j))
        classifier.AddDocuments(docs, gender, age)
    classifier.Train()
    classifier.Save()
    