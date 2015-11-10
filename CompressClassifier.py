#!/usr/bin/python

import pickle
import sys
import operator
import codecs
from data import ReadMeta
from math import log
import data
import util_functions

class CompressClassifier:

	def GuessAge(self, documents):
		features = [18,25,35,50,65]
		bits = {18:0,25:0,35:0,50:0,65:0}
		for document in documents:
			tokens =  util_functions.DocumentToTokens(document)
			for t in tokens:
				for feat in features:
					bits[feat]=bits[feat]+log(self.GetPosition(t, feat)+1)/log(2)
		bits_array=[bits[18],bits[25],bits[35],bits[50],bits[65]]
		minbits = min(bits_array)
		posmin = -1
		for feat in features:
			if(minbits == bits[feat]):
				posmin = feat  		
		return posmin

	def GuessGender(self, documents):
		features = [0,1]
		bits = {0:0,1:0}
		for document in documents:
			tokens =  util_functions.DocumentToTokens(document)
			for t in tokens:
				for feat in features:
					bits[feat]=bits[feat]+log(self.GetPosition(t, feat)+1)/log(2)
		bits_array=[bits[0],bits[1]]
		minbits = min(bits_array)
		posmin = -1
		for feat in features:
			if(minbits == bits[feat]):
				posmin = feat  						
		return posmin

	def Guess(self, documents):
		return (self.GuessGender(documents), self.GuessAge(documents))
	
	# Retrieves the position of the given word in the vocabulary for the given feature
	def GetPosition(self, word, feat):
		if(self.pos[feat].has_key(word)):
			return self.pos[feat][word]
		else:
			return self.numwords + 1

	def AddDocuments(self, documents, gender, age):
		for document in documents:
			tokens =  util_functions.DocumentToTokens(document)
			for t in tokens:
				self.AddWordInHash(t, age, gender)
	
	def Train(self):
		self.ObtainPosForWords()

	# AddWord  
	def AddWordInHash(self, word, age, gender):
		if(not self.voc.has_key(word)):
			self.voc[word]={0:0,1:0,18:0,25:0,35:0,50:0,65:0}
		self.voc[word][gender] = self.voc[word][gender]+1
		self.voc[word][age] = self.voc[word][age]+1
		self.numwords = self.numwords+1

	def ObtainPosForWords(self):
		rangefeat = [0,1,18,25,35,50,65]	
		for feat in rangefeat:
			for word in self.voc:
				if(self.voc[word][feat]>0):
					self.pos[feat][word]=self.voc[word][feat]
			sorted_words = sorted(self.pos[feat].iteritems(), key=operator.itemgetter(1), reverse=True)
			for index, w in enumerate(sorted_words):
				self.pos[feat][w[0]]=index	

	def Save(self):
		out_fp = open(self.basename+".hvoc","w")
		pickle.dump(self, out_fp)
		out_fp.close()

	def __init__(self, basename):
		self.basename = basename
		self.voc = {}
		self.pos = {0:{},1:{},18:{},25:{},35:{},50:{},65:{}}
		self.numwords = 0
			
