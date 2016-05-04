from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# from django.db import models
from django.utils import timezone
import time
from .sentAnalyzeTwitter import *
from .sentAnalyzeFacebook import *
from .models import *
import ast
# from .sentEngine import *

def index(request):
	template = loader.get_template('index.html')
	mcq = MostCommonQuery.getLog()
	mcqList = []
	for (q,f) in ast.literal_eval(mcq.most_common):
		mcqList.append({"text": q, "freq": f})
	context = {'media_list': ['twitter','facebook'], 'most_common_query': mcqList}
	print mcqList
	return HttpResponse(template.render(context, request))

def result(request):
	#parameters
	template = loader.get_template('result.html')
	query = request.GET['q']
	media = request.GET['media']

	#get social media data with sentiments
	N = 10
	if media == "twitter":
		result = analyzeNewTweets(query, N)
		reasons = generateReasonForTweetSent(result)
		wordCloud = getWordCloud(reasons)
	else:
		# your own facebook api key
		token = ""
		result = analyzeNewFBPosts(query, N, token)
		reasons = generateReasonForTweetSent(result)
		wordCloud = getWordCloud(reasons)

	#retrive some previous record
	posC = len(result["positive"])
	neuC = len(result["neutral"])
	negC = len(result["negative"])
	print "pos/neu/neg = " + str(posC) + "/" + str(neuC) + "/" + str(negC)
	dataset = QueryResult.objects.all()
	for data in dataset:
		if data.result_query.query_text == query:
			print data.result_query.query_text
			posC += data.result_pos
			neuC += data.result_neu
			negC += data.result_neg

	#save record
	qrd = QueryRecord(query_text=query, query_media=media, query_time=timezone.now())
	qrd.save()
	qrt = QueryResult(result_pos=len(result["positive"]), result_neu=len(result["neutral"]), result_neg=len(result["negative"]), result_query=qrd)
	qrt.save()
	MostCommonQuery.newLog()

	print "pos/neu/neg = " + str(posC) + "/" + str(neuC) + "/" + str(negC)
	
	#for each sentiments
	context = {
		"posCount": posC,
		"neuCount": neuC,
		"negCount": negC,
		"positive": result["positive"],
		"neutral": result["neutral"],
		"negative": result["negative"],
		"query": query,
		"reasons": reasons,
		"wordCloud": wordCloud,
		"summary": result["summary"],
	}
	return HttpResponse(template.render(context, request))

def sentEngine(request):
	return result(request)
