#!/usr/bin/python

import pickle
import util_functions

ENGLISH = 0
SPANISH = 1

FEMALE = 0
MALE = 1

AGES = [18, 25, 35, 50, 65]
GENDERS = [FEMALE, MALE]

class EntropyClassifier:
    def __init__(self, filename, load = False):
        self.filename = filename
        self.num_words = {}
        self.total_docs = {}

    def GuessAge(self, documents):
				num_wordsA = {}
				total_docsA = {}
				for age in AGES:
				    numw=0
				    totdoc=0
				    for gender in GENDERS:
				        numw = numw + self.num_words.get((gender,age),0)
				        totdoc = totdoc + self.total_docs.get((gender,age),0)
				    num_wordsA[age]=numw
				    total_docsA[age]=totdoc
				best_key = -1
				best = 10000000000
				entropy = 0
				for document in documents:
					  entropy += util_functions.Entropy(document)
				entropy /= len(documents)
		
		 		for key in num_wordsA.keys():
		 			diff = abs(float(num_wordsA[key])/total_docsA[key] - entropy)
					if diff < best:
						best_key = key
						best = diff
				return best_key
        
        #return self.Guess(documents)[1]

    def GuessGender(self, documents):

				num_wordsG = {}
				total_docsG = {}
				for gender in GENDERS:
				    numw=0
				    totdoc=0
				    for age in AGES:
				        numw = numw + self.num_words.get((gender,age),0)
				        totdoc = totdoc + self.total_docs.get((gender,age),0)
				    num_wordsG[gender]=numw
				    total_docsG[gender]=totdoc
				best_key = -1
				best = 10000000000
				entropy = 0
				for document in documents:
					  entropy += util_functions.Entropy(document)
				entropy /= len(documents)
		
		 		for key in num_wordsG.keys():
		 			diff = abs(float(num_wordsG[key])/total_docsG[key] - entropy)
					if diff < best:
						best_key = key
						best = diff
				return best_key


        #return self.Guess(documents)[0]

    def Guess(self, documents):
        best_key = (-1, -1)
        best = 1000000000
        entropy = 0
        for document in documents:
            entropy += util_functions.Entropy(document)
        entropy /= len(documents)
        for key in self.num_words.keys():
            diff = abs(float(self.num_words[key])/self.total_docs[key] - entropy)
            if diff < best:
                best_key = key
                best = diff
        return best_key

    def Train(self):
        pass

    def Save(self):
        out_fp = open(self.filename+".entropy", "w")
        pickle.dump(self, out_fp)
        out_fp.close()

    def AddDocuments(self, documents, gender, age):
        entropy = 0
        for document in documents:
            entropy += util_functions.Entropy(document)
        entropy /= len(documents)
        self.num_words[(gender, age)] = self.num_words.get((gender, age), 0) + entropy
        self.total_docs[(gender, age)] = self.total_docs.get((gender, age), 0) + len(documents)