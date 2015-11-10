#!/usr/bin/python

import pickle
import util_functions


ENGLISH = 0
SPANISH = 1

FEMALE = 0
MALE = 1

AGES = [18, 25, 35, 50, 65]
GENDERS = [FEMALE, MALE]


class WordCountClassifier:
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
		total_words = 0
		for document in documents:
			a, _ = util_functions.CountWords(document)
			total_words += a

 		for key in num_wordsA.keys():
			diff = abs(float(num_wordsA[key])/total_docsA[key] - total_words)
			if diff < best:
				best_key = key
				best = diff
		return best_key

#		return self.Guess(documents)[1]

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
		total_words = 0
		for document in documents:
			a, _ = util_functions.CountWords(document)
			total_words += a

 		for key in num_wordsG.keys():
			diff = abs(float(num_wordsG[key])/total_docsG[key] - total_words)
			if diff < best:
				best_key = key
				best = diff
		return best_key


		#return self.Guess(documents)[0]

	def Guess(self, documents):
		best_key = (-1, -1)
		best = 1000000000
		total_words = 0
		for document in documents:
			a, _ = util_functions.CountWords(document)
			total_words += a
		for key in self.num_words.keys():
			diff = abs(float(self.num_words[key])/self.total_docs[key] - total_words)
			if diff < best:
				best_key = key
				best = diff
		return best_key

	def Train(self):
		pass

	def Save(self):
		out_fp = open(self.filename+".count", "w")
		pickle.dump(self, out_fp)
		out_fp.close()

	def AddDocuments(self, documents, gender, age):
		total_words = 0
		for document in documents:
			a, _ = util_functions.CountWords(document)
			total_words += a
    		self.num_words[(gender, age)] = self.num_words.get((gender, age), 0) + total_words
    		self.total_docs[(gender, age)] = self.total_docs.get((gender, age), 0) + 1

class WordCountNormalizedClassifier:
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
		total_words = 0
		word_count = 1
		for document in documents:
			a, b = util_functions.CountWords(document)
			total_words += a
			word_count += b
		for key in num_wordsA.keys():
			diff = abs(float(num_wordsA[key])/total_docsA[key] - float(total_words)/word_count)
			if diff < best:
				best_key = key
				best = diff
		return best_key


#		return self.Guess(documents)[1]

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
		total_words = 0
		word_count = 1
		for document in documents:
			a, b = util_functions.CountWords(document)
			total_words += a
			word_count += b
		for key in num_wordsG.keys():
			diff = abs(float(num_wordsG[key])/total_docsG[key] - float(total_words)/word_count)
			if diff < best:
				best_key = key
				best = diff
		return best_key
#		return self.Guess(documents)[0]

	def Guess(self, documents):
		best_key = (-1, -1)
		best = 1000000000
		total_words = 0
		word_count = 1
		for document in documents:
			a, b = util_functions.CountWords(document)
			total_words += a
			word_count += b
		for key in self.num_words.keys():
			diff = abs(float(self.num_words[key])/self.total_docs[key] - float(total_words)/word_count)
			if diff < best:
				best_key = key
				best = diff
		return best_key

	def Train(self):
		pass

	def Save(self):
		out_fp = open(self.filename+".ncount", "w")
		pickle.dump(self, out_fp)
		out_fp.close()

	def AddDocuments(self, documents, gender, age):
		total_words = 0
		word_count = 1
		for document in documents:
			a, b = util_functions.CountWords(document)
			total_words += a
			word_count += b
    		self.num_words[(gender, age)] = self.num_words.get((gender, age), 0) + total_words
    		self.total_docs[(gender, age)] = self.total_docs.get((gender, age), 0) + word_count
