#!/usr/bin/python

import pickle
import util_functions
from math import log

ENGLISH = 0
SPANISH = 1

FEMALE = 0
MALE = 1

AGES = [18, 25, 35, 50, 65]
GENDERS = [FEMALE, MALE]

class MTFClassifier:
    def __init__(self, filename):
        self.total_info = {}
        self.total_docs = {}
        self.filename = filename

    def GuessAge(self, documents):
        total_infoA = {}
        for age in AGES:
				    totinfo=0
				    for gender in GENDERS:
				        totinfo = totinfo + self.total_info.get((gender,age),0)
				    total_infoA[age]=totinfo
        total_info = 0
        for document in documents:
            num_words, total_words = util_functions.CountWords(document)
            if total_words == 0: continue
            words = util_functions.DocumentToTokens(document)
            mtfl = {}
            pos = total_words + 1
            info = 0
            for w in words:
                res = pos - mtfl.get(w, total_words)
                info -= log(res)/log(2)
                mtfl[w] = pos
                pos += 1
            info /= total_words
            total_info += info
        total_info /= len(documents)
        best_key = None
        best = 1000000
        for key in total_infoA.keys():
            diff = abs(float(total_infoA[key]) - total_info)
            if diff < best:
                best_key = key
                best = diff
        return best_key

        #return self.Guess(documents)[1]

    def GuessGender(self, documents):
        total_infoG = {}
        for gender in GENDERS:
				    totinfo=0
				    for age in AGES:
				        totinfo = totinfo + self.total_info.get((gender,age),0)
				    total_infoG[gender]=totinfo
        total_info = 0
        for document in documents:
            num_words, total_words = util_functions.CountWords(document)
            if total_words == 0: continue
            words = util_functions.DocumentToTokens(document)
            mtfl = {}
            pos = total_words + 1
            info = 0
            for w in words:
                res = pos - mtfl.get(w, total_words)
                info -= log(res)/log(2)
                mtfl[w] = pos
                pos += 1
            info /= total_words
            total_info += info
        total_info /= len(documents)
        best_key = None
        best = 1000000
        for key in total_infoG.keys():
            diff = abs(float(total_infoG[key]) - total_info)
            if diff < best:
                best_key = key
                best = diff
        return best_key
#        return self.Guess(documents)[0]

    def Guess(self, documents):
        total_info = 0
        for document in documents:
            num_words, total_words = util_functions.CountWords(document)
            if total_words == 0: continue
            words = util_functions.DocumentToTokens(document)
            mtfl = {}
            pos = total_words + 1
            info = 0
            for w in words:
                res = pos - mtfl.get(w, total_words)
                info -= log(res)/log(2)
                mtfl[w] = pos
                pos += 1
            info /= total_words
            total_info += info
        total_info /= len(documents)
        best_key = None
        best = 1000000
        for key in self.total_info.keys():
            diff = abs(float(self.total_info[key]) - total_info)
            if diff < best:
                best_key = key
                best = diff
        return best_key

    def Train(self):
        pass

    def Save(self):
        out_fp = open(self.filename+".mtf", "w")
        pickle.dump(self, out_fp)
        out_fp.close()

    def AddDocuments(self, documents, gender, age):
        total_info = 0
        for document in documents:
            num_words, total_words = util_functions.CountWords(document)
            if total_words == 0: continue
            words = util_functions.DocumentToTokens(document)
            mtfl = {}
            pos = total_words + 1
            info = 0
            for w in words:
                res = pos - mtfl.get(w, total_words)
                info -= log(res)/log(2)
                mtfl[w] = pos
                pos += 1
            info /= total_words
            total_info += info
        total_info /= len(documents)
        self.total_info[(gender, age)] = self.total_info.get((gender, age), 0) + total_info