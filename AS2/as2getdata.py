import twitter
import io, json
import auth
import datetime
# import simplejson
import gnp

# set search topic
q = 'oscar'
# q = 'virtual reality'
# q = 'internet of things'
# q = 'artificial intelligence'
# q = 'research'

print "topic: " + q

#get twitter data
twitter_api = auth.login()
print twitter_api
twitter_stream = twitter.TwitterStream(auth = twitter_api.auth)
print "got stream api"

stream = twitter_stream.statuses.filter(track = q)
print "got stream"


result_data = {"0": 0}
result_data.clear()

i = 0;
for tweet in stream:
	key = 'tweet' + str(i)
	result_data[key] = tweet['text']
	# print result_data
	i = i + 1
	if i % 10 == 0:
		time = datetime.datetime.now()
		with open('./AS2data/captured_tweets_stream_' + time.strftime("%Y%m%d_%H%M%S") + '.json', 'w') as outfile:
			json.dump(result_data, outfile, indent = 4)
		break

# get google data
# gnews = gnp.get_google_news(gnp.EDITION_ENGLISH_US)
gnews = gnp.get_google_news_query(q)

time = datetime.datetime.now()
with open('./AS2data/google_news_' + time.strftime("%Y%m%d_%H%M%S") + '.json', 'w') as outfile:
	json.dump(gnews, outfile, indent = 4)

