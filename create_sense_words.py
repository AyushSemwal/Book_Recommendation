import sys
import sensegram
import json

sense_vectors_fpath = "/Users/rickysemwal/Documents/DVA/Project/model/wiki.txt.clusters.minsize5-1000-sum-score-20.sense_vectors"
sv = sensegram.SenseGram.load_word2vec_format(sense_vectors_fpath, binary=False)

keywords_file = open("/Users/rickysemwal/Documents/DVA/Project/win_top_keywords.txt",'r')
output_file = open("/Users/rickysemwal/Documents/DVA/Project/win_sense_words.txt",'w+',200)

for line in keywords_file:
	fields = line.rstrip().split("\t")
	words = fields[1].lstrip().split(" ")
	for i in range(len(words)):
		words[i] = words[i].lower()
	output_file.write("%s\t"%(fields[0]))
	for word in words[:5]:
		if (fields[0][0] == "{"):
			continue
		if (word == "none"):
			break
		else:
			count_1 = 0
			for sense_id, prob in sv.get_senses(word):
				count = 0
				for rsense_id, sim in sv.wv.most_similar(sense_id):
					if rsense_id[:-2].lower() not in words:
						words.append(rsense_id[:-2].lower())
						count += 1
					if (count == 3):
						break
				count_1 += 1 
				if (count_1 == 3):
					break
	sense_string = " ".join(words)
	# print(fields[0] + "\t" + sense_string)
	output_file.write("%s\n"%(sense_string))
	output_file.flush()

