# from __future__ import division
# import nltk
# from nltk.corpus import wordnet as wn
# from nltk.corpus import brown
# import math
# import numpy as np
import sys
from sematch.semantic.similarity import WordNetSimilarity
import sensegram
import json

wns = WordNetSimilarity()

sense_vectors_fpath = "/Users/rickysemwal/Documents/DVA/Project/model/wiki.txt.clusters.minsize5-1000-sum-score-20.sense_vectors"
sv = sensegram.SenseGram.load_word2vec_format(sense_vectors_fpath, binary=False)

top_words = {}
book_name = {}

candidate_friends = []
friend_book_matches = []

keywords_file = open("/Users/rickysemwal/Documents/DVA/Project/top_keywords.txt", 'r')

# creating source book's word cloud

for line in keywords_file:
	fields = line.rstrip().split("\t")
	top_words[fields[0]] = fields[1].split(" ")

source_word_cloud = top_words["0786817879"]
source_word_cloud = source_word_cloud[:-1]

for i in range(len(source_word_cloud)):
	source_word_cloud[i] = source_word_cloud[i].lstrip()

#creating query words cloud

query_word_cloud = []
for word in source_word_cloud[:5]:
	for sense_id, prob in sv.get_senses(word):
		for rsense_id, sim in sv.wv.most_similar(sense_id):
			query_word_cloud.append(rsense_id[:-2])

query_word_cloud = query_word_cloud + source_word_cloud

print(len(query_word_cloud))

# building a candidate books set

candidate_book_set = []
for word_2 in query_word_cloud:
	for isbn, words in top_words.items():
		for word_1 in words:
			word_1 = word_1.lstrip()
			if ((round(wns.word_similarity(word_1,word_2),2) > 0.80) and (isbn not in candidate_book_set)):
				candidate_book_set.append((isbn,round(wns.word_similarity(word_1,word_2),2)))
				break

print(len(candidate_book_set))

# finding friend's closeness 
json_file = open('/Users/rickysemwal/Documents/DVA/Project/dat.json')
data_file = json.load(json_file)

friend_list = []
for key, value in data_file["79906948"]["friends"].items():
	friend_list.append(value)

friends_word_cloud = {}
for friend in friend_list:
	if (str(friend) not in data_file):
		continue
	for book in (data_file[str(friend)]["books"]):
		if ((type(data_file[str(friend)]["books"][book]["isbn"]) is str)):
			print(data_file[str(friend)]["books"][book]["isbn"])
			word_cloud = (top_words[data_file[str(friend)]["books"][book]['isbn']])[:-1]
			print(word_cloud)
		for i in range(len(word_cloud)):
			word_cloud[i] = word_cloud[i].lstrip()
			word_cloud_2 = []
		for word in word_cloud[:5]:
			for sense_id, prob in sv.get_senses(word):
				for rsense_id, sim in sv.wv.most_similar(sense_id):
					word_cloud_2.append(rsense_id[:-2])
		word_cloud_2 = word_cloud_2 + word_cloud
		friends_word_cloud[friend] = word_cloud_2

friend_closeness = {}

for friend in friend_list:
	closenss_score = 0
	if (str(friend) not in data_file):
		continue
	for tag_1 in query_word_cloud:
		for tag_2 in friends_word_cloud[friend]:
			if (round(wns.word_similarity(tag_1,tag_2),2) >= 0.40):
				closenss_score += 1
	friend_closeness[friend] = round(closenss_score/(len(query_word_cloud)*len(friends_word_cloud)),2)

friend_closeness
# overall score
final_score = {}

for pair in candidate_book_set:
	final_score[pair[0]] = 0
	number_of_friends = 0
	for friend in friend_list:
		if (str(friend) not in data_file):
			continue
		if (pair[0] in data_file[str(friend)]["books"].values()):
			final_score[pair[0]] += pair[1]*friend_closeness[friend]
		else 
	final_score[pair[0]] = round((final_score[pair[0]]),2)

