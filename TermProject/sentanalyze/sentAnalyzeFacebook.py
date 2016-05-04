import os

# os.environ['CLASSPATH'] = '/Users/LiuShuchang/Documents/workspace/textmining/restfb-1.18.1/restfb-1.18.1.jar'
os.environ['CLASSPATH'] = '/Users/LiuShuchang/Documents/workspace/eclipse/MiningFacebook/Miner.jar'
# os.environ['JAVA_HOME'] = '/usr/libexec/java_home'
# print os.environ['CLASSPATH']
# import jnius_config

# jnius_config.add_options('-Xrs', '-Xmx4096M')
# jnius_config.set_classpath('.', '/Users/LiuShuchang/Documents/workspace/eclipse/MiningFacebook/bin')

from jnius import autoclass
import json
import urllib2
import urllib
import requests

langDetectionUrl = "http://api.datumbox.com/1.0/LanguageDetection.json"
sentAnalyzeUrl = "http://api.datumbox.com/1.0/SentimentAnalysis.json"

# Use your own datum api key
api_key = ""
def datumRequest(req_url, req_data):
	response = requests.post(req_url, params = {'api_key': api_key, "text": req_data})
	return json.loads(response.text)
	# payload = "text=" + req_data
	# req = urllib2.Request(url=req_url + "?" + api_key, data=payload)
	# print req
	# # r = requests.post("http%3A%2F%2Fwww.sentiment140.com%2Fapi%2FbulkClassifyJson%3Fappid%3Dsliu124%40syr.edu", params = payload)
	# res = urllib2.urlopen(req_url)
	# print res.read()
	# res = res.read().decode("UTF-8", 'ignore')
	# res = json.loads(res)


def getLanguage(req_data):
	print "detect language"
	res = datumRequest(langDetectionUrl, req_data[0:10])
	if "output" in res:
		output = res["output"]
		if "result" in output:
			return output["result"]
		else:
			print "result:" + json.dumps(output)
			return "none"
	else:
		print "language detection fail"
		return "none"

def getSentiment(req_data):
	print "analyze sentiment"
	res = datumRequest(sentAnalyzeUrl, req_data)
	if "output" in res:
		output = res["output"]
		return output["result"]
	else:
		print "sentiment analysis fail"
		return "none"

def retriveData(topic, number, token):
	Miner = autoclass('edu.lsc.smm.Miner')
	print Miner
	data = Miner.retriveData(topic, number, token)
	data = json.loads(data)
	posts = []
	index = 0;
	for post in data:
		# print json.dumps(post, indent = 4)
		if "message" in post:
			# print post["message"]
			#filter language of en
			lang = getLanguage(post["message"])
			if lang == "en":
				posts.append(post["message"])
				# print post
			else:
				print lang + " not english"
		else:
			print "No message"
		index += 1
		if index % 10 == 0:
			print str(len(posts)) + "/" + str(index) + "/" + str(len(data))
		if len(posts) >= number:
			break;
	# print json.dumps(data, indent = 4)
	print "Got " + str(len(posts)) + " posts."
	return posts

from naivesumm import NaiveSummarizer

def analyzeNewFBPosts(topic, number, token):
	payloaddata = retriveData(topic, number, token)
	# summary
	summerizer = NaiveSummarizer()
	textdoc = ""
	for data in payloaddata:
		textdoc += (data + ". ")
	summ = summerizer.summarize(textdoc, 4)
	print "summarize: " + summ
	# result into json
	posList = []
	neuList = []
	negList = []
	index = 0
	for post in payloaddata:
		res = getSentiment(post)
		if res is not "none":
			if res == "positive":
				posList.append(post)
			if res == "negative":
				negList.append(post)
			# if res == "neutral":
			# 	neuList.append(post)
		index += 1
		print str(index) + "/" + str(len(payloaddata))
	# print json.dumps(results, indent = 4)
	return {"positive": posList, "negative": negList, "neutral": neuList, "summary": summ}

# analyzeNewPosts('AI', 'CAACEdEose0cBAJPsfkUp71nxbZAFfCjgE1VPZAN3h5vE68T5PD9Ju00d8eedNqKaooZAVCU7AbYJYZAWNJ1sWfXO2WOMFHu4qxrS75GIUattFwZB8x0g4yoqzzZBxZCSqcyQnRUz5IrB3B9gKyvQfSf1UHKZBGNgcNFikjg3OhNK5pjYdM1ZALmu0Y6yuc5iCXXObtHEJkNaXfwZDZD')