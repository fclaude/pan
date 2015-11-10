#!/usr/bin/python

import xml.parsers.expat
import data
import pickle
import sys
import unicodedata
import types
import os
import util_functions
import warnings

def remove_accents(input_str):
	nkfd_form = unicodedata.normalize('NFKD',input_str)
	only_ascii = nkfd_form.encode('ASCII', 'ignore')
	return only_ascii


if __name__ == "__main__":
	warnings.simplefilter("ignore")

	if len(sys.argv) != 3:
		print "usage: %s <file list> <output basename>" % (sys.argv[0])
		sys.exit(0)

	extras = [-1, -1, -1]
	conversations = []
	conv_start = [False] # terrible, terrible hack
	conv_ids = []


	def start_element(name, attrs):
		if name == "author":
			if attrs["lang"].lower() == "en":
				extras[0] = data.ENGLISH
			else:
				extras[0] = data.SPANISH

		if name == "document":
			conv_start[0] = True
			conversations.append("")
			conv_ids.append(str(attrs["id"]))		


	def end_element(name):
		if name == "document":
			conv_start[0] = False


	def char_data(data):
		if conv_start[0]:
			for d in data:
				if ord(d) < 256:
					conversations[-1] += d


	results = {}
	fp = open(sys.argv[1] + "/truth.txt")
	for l in fp.readlines():
		datar = l[:-1].split(":::")
		results[datar[0]] = (data.AgeStringToInt(datar[2]),datar[1])


	path=sys.argv[1]
	dirList=os.listdir(path)
	files = []
	for root, subFolders, fs in os.walk(path):
		#print root, subFolders,fs
		for f in fs:
			if(f[-4:]=='.xml'):
				files.append(os.path.join(root,f))
		

	out_fp = open(sys.argv[2]+".data", "w")
	outm_fp = open(sys.argv[2]+".meta","w")

	pos = 0
	offs = 0
	meta = data.Meta()
	meta.lengths.append(0)
	for f in files:
		conversations = []
		extras = [-1, -1, -1]

		conv_start = [False]
		conv_ids = []
		user_id = f.split("/")[-1][:-4]
		if results.has_key(user_id):
			extras[1] = results[user_id][0]
			if results[user_id][1].lower() == "male":
				extras[2] = data.MALE
			else:
				extras[2] = data.FEMALE

		print "Parsing file %s for user %s" % (f, user_id)
		meta.ids.append(user_id)
		user_num = len(meta.ids) - 1
		fp = open(f)
		p = xml.parsers.expat.ParserCreate()
		p.StartElementHandler = start_element
		p.EndElementHandler = end_element
		p.CharacterDataHandler = char_data
		p.Parse(fp.read())
		meta.conv_ids.append(conv_ids)
		meta.ages.append(extras[1])
		meta.genders.append(extras[2])
		meta.langs.append(extras[0])
		meta.num_convs.append(len(conversations))
		meta.conv_offset.append(offs)
		for i in xrange(len(conversations)):
			convers = conversations[i]
			#print type(convers), user_id, i, convers, types.UnicodeType
			convers = util_functions.DocumentToTxt(convers)
			if(type(convers)==types.UnicodeType):
				convers = remove_accents(convers)
			meta.lengths.append(pos+len(convers))
			pos += len(convers)
			out_fp.write(convers)
			offs += 1

	pickle.dump(meta, outm_fp, -1)
	out_fp.close()
	outm_fp.close()
	



