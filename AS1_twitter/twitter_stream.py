import twitter
import io, json
import auth
import datetime

twitter_api = auth.login()

print twitter_api

twitter_stream = twitter.TwitterStream(auth = twitter_api.auth)

print "got stream api"

q = 'Virtual Reality,VR'

print "topic" + q

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
	if i % 100 == 0:
		time = datetime.datetime.now()
		with open('captured_tweets_stream_' + time.strftime("%Y%m%d_%H%M%S") + '.json', 'w') as outfile:
			json.dump(result_data, outfile, indent = 4)
			print "file updated" + str(i)
		result_data.clear()
	if i >= 1000:
		break