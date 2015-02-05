import logging
import sys
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from glove import Glove 

import collections


def get_label(test_vec):
	sim = dict()
	min_label = 0
	min_sim = 0
	max_sim = 0
	output_values = []

	for l in labels:
		curr_sim = 0
		min_sim = 0
		#print l
		for vecs in labels[l]:
			curr_sim = (cosine_similarity(vecs, test_vec))
			if min_sim < abs(curr_sim):
				min_sim = abs(curr_sim)
		if max_sim < min_sim:
			max_sim = min_sim
			min_label = l
		sim[l] = min_sim
	#print sim
	result[min_label] +=1
	return sim
	

def train_sentiment(phrase):
	global model, phrases, labels, result
	
	for i in range(0,11):
		labels[i] = []	
		result[i] = 0
	labels[12] = []
	result[12] = 0

	for line in phrase:
		words = line.strip().split()
		#print words
		l = int(words[1])
		w = words[0].replace('*','')
		#print w
		#print l
		if w in model.dictionary:
			labels[l].append(model.word_vectors[model.dictionary[w]])
		

def test_sentiment(test_phrase):
	global keywords
	for line in test_phrase:
		line = line.strip()
		words = line.split("\t")
		sws = words[0].lower()
		flag = True
		#for k in keywords:
		#	if k in sws:
		#		flag = True
		#		break
		#if any( k in sws for k in keywords ) == False:
		if flag == True:
			line_vec = [0]*200
			for w in words[0].split():
				#print w
				if w != "URL":
					if w in model.dictionary:
						#print w
						line_vec = np.add(line_vec, model.word_vectors[model.dictionary[w]])
					else:
						w = w.lower()
						if w in model.dictionary:
                                                #print w
                                                	line_vec = np.add(line_vec, model.word_vectors[model.dictionary[w]])
			l = get_label(line_vec)
			print line.replace(",","") + "," + str(l[1]) + "," + str(l[2]) + "," + str(l[3]) + "," + str(l[4]) + "," + str(l[5]) + "," + str(l[6]) + "," + str(l[7]) + "," + str(l[8]) + "," + str(l[9]) + "," + str(l[10]) + "," + str(l[12])


def main():
    global model, phrases, labels, result, keywords
    labels = dict()
    phrases = dict()
    result = dict()
    keywords = ["cleanindia","cleanindiacampaign","mycleanindia","swachhbharatmission","swachbharatmission","cleanupindia","swachbharat","swach bharat","swachh bharat", "clean","swachh", "swatchta", "abhiyaan"]
    print 'Loading the word2vec model'
    training = sys.argv[1]
    model = Glove.load_stanford(training)
    print ' Loaded the vectors corpus'
    #model.init_sims(replace=True)
   
    train_phrase = open(sys.argv[2])
    test_phrases = open(sys.argv[3])
    train_sentiment(train_phrase) 
    #print labels
    test_sentiment(test_phrases)
    train_phrase.close()
    test_phrases.close()
    print result
    #print 'Added all word vecs for each sentence'
   

main()

