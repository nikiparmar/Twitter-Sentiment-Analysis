

import gensim, logging
import sys
import re
import os
from sklearn.metrics.pairwise import cosine_similarity

import collections

def label_tag(value):
	if value < 0.4:
		return 1
	if value > 0.6:
		return 3
	return 2


def get_label(test_vec):
	sim = dict()
	min_label = 0
	min_sim = 99999999

	for l in labels:
		curr_sim = 0
		print l
		for vecs in labels[l]:
			curr_sim += (cosine_similarity(vecs, test_vec))
		if min_sim < abs(curr_sim):
			min_sim = abs(curr_sim)
			min_label = l
		sim[l] = curr_sim
	print sim
	return min_label
	

def train_sentiment(phrase, slabels):
	global model, phrases, labels
	labels[1] = [] 
	labels[2] = []
	labels[3] = []
	
	sentence = ""	
	for line in phrase:
		words = line.strip().split("|")
		print words
		phrases[words[1]] = words[0]

	for line in slabels:
		words = line.strip().split("|")
		print words
		l = label_tag(float(words[1]))
		if words[0] in phrases:
			sentence = phrases[words[0]]
			line_vec = 0
			for w in sentence.split(" "):
				if w in model:
					line_vec+= model[w]
			labels[l].append(line_vec)
			print sentence + " " + str(line_vec)		

def test_sentiment(test_phrase):
	for line in test_phrase:
		words = line.strip().split("|")
		line_vec = 0
		for w in words[0]:
			if w in model:
				line_vec += model[w]
		l = get_label(line_vec)
		print words[0] + " " + str(l)


def main():
    global model, phrases, labels
    labels = dict()
    phrases = dict()
    print 'Loading the google news corpus'
    training = sys.argv[1]
    model = gensim.models.Word2Vec.load_word2vec_format(training,binary=False)
    print ' Loaded the news corpus'
    model.init_sims(replace=True)
   
    train_phrase = open(sys.argv[2])
    train_label = open(sys.argv[3])
    test_phrases = open(sys.argv[4])
    train_sentiment(train_phrase, train_label) 
    test_sentiment(test_phrases)
print 'Added all word vecs for each sentence'
   

main()

