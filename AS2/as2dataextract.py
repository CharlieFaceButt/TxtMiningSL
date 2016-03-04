import json
import os
from collections import Counter
from nltk.tokenize import TweetTokenizer
from nltk import *
from nltk.corpus import gutenberg

path = './AS2data'

def get_people(sent):
	person = []
	for subtree in sent.subtrees(filter=lambda t: t.label() == 'PERSON'):
	    for leave in subtree.leaves():
	        person.append(leave)
	print person
	return person

# tweets
files = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path,i)) and \
         'captured_tweets_' in i]
print str(len(files)) + " files loaded"

tweets_ner = {}
tweets_sents = {}
tweets_person = {}
# tweets_ner = ""
i = 0

for infile in files:
	# for each file
	with open(os.path.join(path,infile)) as json_file:
		# get tweets
		data = json.load(json_file)
		for key, value in data.items():
			# for each tweet
			# tokenize the sentence
			sents = sent_tokenize(value)

			for j in range(len(sents)):
				# for each sentence
				tokens = word_tokenize(sents[j])
				# POS
				POS_tagged_tokens = pos_tag(tokens)
				tk = 'tweet' + str(i)
				tweets_sents[tk] = sents[j]
				# NER
				tweets_ner[tk] = ne_chunk(POS_tagged_tokens, binary = False)
				# get person
				tweets_person[tk] = get_people(tweets_ner['tweet' + str(i)])
				i = i + 1
				if i >= 50:
					break
			print key + " is analyzed"	
			if i >= 50:
				break
		print "file " + infile + " is analyzed"
		if i >= 50:
			break

with open(path + '/tweets_after_ner.json', 'w') as outfile:
			json.dump(tweets_ner, outfile, indent = 2)
with open(path + '/tweets_before_ner.json', 'w') as outfile:
			json.dump(tweets_sents, outfile, indent = 2)
with open(path + '/tweets_person.json', 'w') as outfile:
			json.dump(tweets_person, outfile, indent = 2)

# google news
files = [index for index in os.listdir(path) if os.path.isfile(os.path.join(path,index)) and \
		 'google_news_' in index]
print str(len(files)) + " google news file loaded"

news_ner = {}
news_sents = {}
news_person = {}
i = 0;

for infile in files:
	# for each file
	with open(os.path.join(path,infile)) as json_file:
		# get news
		data = json.load(json_file)
		# get stories
		stories = data['stories']
		for story in stories:
			# for each story get sentences
			sents = sent_tokenize(story['content_snippet'])
			for j in range(len(sents)):
				# for each sentence get tokens
				tokens = word_tokenize(sents[j])
				# POS
				POS_tagged_tokens = pos_tag(tokens)
				# before NER
				nk = 'news' + str(i)
				news_sents[nk] = sents[j]
				# NER
				news_ner[nk] = ne_chunk(POS_tagged_tokens, binary = False)
				# get person
				news_person[nk] = get_people(news_ner[nk])
				i = i + 1
				if i >= 50:
					break
			print "news " + str(i) + " is analyzed"
			if i >= 50:
				break
	print "file " + infile
	if i >= 50:
		break

with open(path + '/news_after_ner.json', 'w') as outfile:
	json.dump(news_ner, outfile, indent = 4)
with open(path + '/news_before_ner.json', 'w') as outfile:
	json.dump(news_sents, outfile, indent = 4)
with open(path + '/news_person.json', 'w') as outfile:
	json.dump(news_person, outfile, indent = 4)
