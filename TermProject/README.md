# Voice of Social Media

Web application that provides understandable visualization of social media text mining results. This app is considered a review and integration of my text mining class content (CIS700 SPRING 2016 SU).

## Functionalities

* User query
* Most common topic ever searched
* Twitter tweets and Facebook posts retrival and preprocessing
* Sentiment analysis
* Find interesting name entities
* Discover relations
* Text summary

## Tools, techniques and their usage

|Techniques|Usage|
|----------|-----|
|[Django](https://www.djangoproject.com)|Project framework|
|Twitter [search API](https://dev.twitter.com/rest/public) & [streaming API](https://dev.twitter.com/streaming/overview)|collect tweets|
|Java [RESTFB API](http://restfb.com)|collect Facebook posts|
|[Pyjnius](http://pyjnius.readthedocs.io/en/latest/)|Python wrapper of java class|
|[NLTK](http://www.nltk.org)|Text to number, NER, text summarization, relation extraction|
|[Sentiment 140 API](http://help.sentiment140.com/api)|Twitter sentiment analysis|
|[DatumBox API](http://www.datumbox.com/machine-learning-api/)|Facebook sentiment analysis, language detection|
|SQLite|Database, default in Django framework|
|[Echarts](https://github.com/ecomfe/echarts), [Zingcharts](http://www.zingchart.com)|Javascript visualization tools|

## A similar application by other developer

[Sentiment Visualization App](https://www.csc.ncsu.edu/faculty/healey/tweet_viz/tweet_app)

# Configurations

## 