#!/usr/bin/python

import pickle
import nltk
from bs4 import BeautifulSoup
from math import log


from CountClassifier import WordCountClassifier, WordCountNormalizedClassifier
from EntropyClassifier import EntropyClassifier
from CompressClassifier import CompressClassifier
from MTFClassifier import MTFClassifier

def GetClassifier(name, basename):
    if name == "WordCountClassifier": return WordCountClassifier(basename)
    if name == "WordCountNormalizedClassifier": return WordCountNormalizedClassifier(basename)
    if name == "EntropyClassifier": return EntropyClassifier(basename)
    if name == "CompressClassifier": return CompressClassifier(basename)
    if name == "MTFClassifier": return MTFClassifier(basename)

def DocumentToTokens(original):
	soup = BeautifulSoup(original.lower())
	original = soup.get_text()
	# print original
	ignore = ['_',',','\t','\n','\'',':','.',';',',']
	pstring=[]
	cstring = ""
	if(len(original)>0):
		#print original, len(original)
		#print original[0]
		status = original[0].isalnum()
		for c in original:
			if c in ignore:
				continue
			if (c==' ') or (status != c.isalnum()):
				if(cstring <> ""):
					pstring.append(cstring)
				cstring = ""
				if(c<>' '):
					status = c.isalnum();
					cstring = cstring + c;
			else:
				cstring = cstring+c
			

	return pstring

def DocumentToTxt(original):
	return " ".join(DocumentToTokens(original))

def CountWords(document):
	words = {}
	doc = DocumentToTokens(document)
	for w in doc:
		words[w] = True
	return (len(words), len(doc))

def LoadClassifier(filename):
	fp = open(filename)
	cl = pickle.load(fp)
	fp.close()
	return cl

def Entropy(document):
    words = DocumentToTokens(document)
    if words == []: return 0
    freqs = {}
    for w in words:
        freqs[w] = freqs.get(w, 0) + 1
    entropy = 0
    for w in freqs.keys():
        entropy -= freqs[w]*log(float(freqs[w])/len(words)) / log(2)
    return entropy / len(words)

def remove_accents(input_str):
	print type(input_str)
	nkfd_form = unicodedata.normalize('NFKD',input_str)
	only_ascii = nkfd_form.encode('ASCII', 'ignore')
	return only_ascii
