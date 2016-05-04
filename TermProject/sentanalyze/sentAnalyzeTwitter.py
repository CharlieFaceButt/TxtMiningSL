# from sklearn.svm import LinearSVC
# from nltk.classify.scikitlearn import SklearnClassifier
from nltk.tokenize import TweetTokenizer
from nltk import *

import twitter
import json
import urllib2
import urllib
import auth

from naivesumm import NaiveSummarizer

def analyzeNewTweets(query, N):
	#normalize input, query should be short, N should not be larger
	#than 500. ?not implemented?

	#collect no more than N data
	tweets = searchAndExtractTweets(query, N)
	print "extracted " + str(len(tweets)) + " tweets"
	# text summarization
	summerizer = NaiveSummarizer()
	textdoc = ""
	for tweet in tweets:
		textdoc += (tweet["text"] + ". ")
	summ = summerizer.summarize(textdoc, 4)
	print "summarize: " + summ
	# sentiment analysis
	payloaddata = json.dumps({'language': 'en', 'data': tweets})
	req = urllib2.Request(url="http://www.sentiment140.com/api/bulkClassifyJson?appid=sliu124@syr.edu", data = payloaddata)
	res = urllib2.urlopen(req)
	# results into json
	res = res.read().decode("UTF-8", 'ignore')
	resdict = json.loads(res)
	negList = []
	neuList = []
	posList = []
	for sent in resdict["data"]:
		if sent["polarity"] == 0:
			negList.append(sent["text"])
		if sent["polarity"] == 4:
			posList.append(sent["text"])
		if sent["polarity"] == 2:
			neuList.append(sent["text"])
	return {"positive": posList, "neutral": neuList, "negative": negList, "summary": summ}


#Get tweets of certain topic
def searchAndExtractTweets(query, number):
	twitter_api = auth.login()
	search_results = []
	count = number
	# See https://dev.twitter.com/docs/api/1.1/get/search/tweets
	print "query: " + query
	# At most 100 tweets allowed
	current_results = twitter_api.search.tweets(q=query, count=100, lang='en')
	meta = current_results["search_metadata"]
	tweets = current_results["statuses"]

	for result in tweets:
		if {"text": result["text"]} in search_results:
			print "duplicated"
			continue
		search_results.append({"text": result["text"]})
		count -= 1
		if count <= 0:
			break;

	print "got " + str(len(search_results)) + " tweets"
	# Compliment tweets by stream
	# twitter_stream = twitter.TwitterStream(auth = twitter_api.auth)
	# stream = twitter_stream.statuses.filter(track = query)
	# print "Compensate tweets number: " + str(count)
	# for newTweet in stream:
	# 	if count > 0:
	# 		if {"text": newTweet['text']} in search_results:
	# 			continue
	# 		search_results.append({"text": newTweet['text']})
	# 		count -= 1
	# 	else:
	# 		break
	return search_results


# def getNE(dList):
# 	reasons = []
# 	tokenizer = TweetTokenizer()
# 	for tweet in dList:
# 		#tokenize
# 		words = tokenizer.tokenize(tweet)
# 		pos_tokens = pos_tag(words)
# 		entities = ne_chunk(pos_tokens, binary = False)
# 		print entities
	# return reasons

# def getRelations(chunk):
# 	for subtree in chunk.subtrees(filter=lambda t: t.label()=='PERSON'):
# 		for leave in subtree

from nltk.sem import relextract
# reason for each sentiment
def reasoning(dList):
	reasonList = []
	tokenizer = TweetTokenizer()
	for tweet in dList:
		print tweet
		# tokenize
		words = tokenizer.tokenize(tweet)
		# get POS tag
		pos_tokens = pos_tag(words)
		# get name entities
		tree = ne_chunk(pos_tokens, binary = False)
		# find relations
		pairs = relextract.tree2semi_rel(tree)
		# get interesting name entities
		reason = []
		for s, tree in pairs:
			reasonStr = ("%s") % tree
			reasonStr = reasonStr.split(" ")
			label = reasonStr[0].replace("(","").strip()
			content = ""
			for wordTag in reasonStr[1:]:
				sp = wordTag.split("/")
				word = sp[0].replace("(","")
				print word
				# content.append(word)
				content += (word + " ")
			# reason: [(label, content)]
			reason.append({"label": label, "content": content})
		# reasonList [reason]
		if len(reason) > 0:
			reasonList.append({"reason": reason})
		print str(len(reasonList)) + "/" + str(len(dList))
	return reasonList

def generateReasonForTweetSent(dList):
	print "generate reasons for positive"
	posReasons = reasoning(dList["positive"])
	print json.dumps(posReasons)

	print "generate reasons for neutral"
	neuReasons = reasoning(dList["neutral"])
	print json.dumps(neuReasons)

	print "generate reasons for negative"
	negReasons = reasoning(dList["negative"])
	print json.dumps(negReasons)

	return {"positive": posReasons, "neutral": neuReasons, "negative": negReasons}

def getWordCloudForSent(sentReasons):
	results = []
	for reason in sentReasons:
		for pair in reason["reason"]:
			results.append(pair["content"])
	return " ".join(results)

def getWordCloud(reasons):
	print "word cloud for positive"
	posWords = getWordCloudForSent(reasons["positive"])
	print "word cloud for positive"
	neuWords = getWordCloudForSent(reasons["neutral"])
	print "word cloud for positive"
	negWords = getWordCloudForSent(reasons["negative"])
	return posWords + " " + neuWords + " " + negWords

	# entities = getNE(list)
	# for chunk in entities:
	# 	rel = getRelations(chunk)
	#find relationship


# # Get training data
# tweets = get_tweets(data)
# # Generate features
# word_features = get_features(tweets)

# # # Construct classifier
# classifier = get_classifier(tweets, word_features)

# test_set = [(extract_features(d, word_features), c) for (d,c) in tweets]
# # classifier.train(test_set)

# print "Accuracy: " + str(nltk.classify.accuracy(classifier, test_set))

# with open("./AS3/testdata.txt") as infile:
# 	data = infile.readlines()
# # # Evaluate test set document
# result = evaluate(data, classifier, word_features)

# # result = []
# # amount = 0
# # for item in data:
# # 	itemstr = item.decode('utf_8', 'ignore')
# # 	tokenizer = TweetTokenizer(itemstr)
# # 	sent = tokenizer.tokenize(itemstr)
# # 	amount += 1
# # 	result.append(classifier.classify_many(extract_features(sent, word_features)))
# # 	if amount % 1000 == 0:
# # 		print str(amount) + " items evaluated."

# # print result
# print str(len(result)) + "results"

# with open("./AS3/result.txt", "w") as outfile:
# 	for item in result:
# 		outfile.write(item[0] + "\n")
#	# print item