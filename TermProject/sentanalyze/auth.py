# Auth login for twitter

import twitter

# XXX: Go to http://dev.twitter.com/apps/new to create an app and get values
# for these credentials, which you'll need to provide in place of these
# empty string values that are defined as placeholders.
# See https://dev.twitter.com/docs/auth/oauth for more information 
# on Twitter's OAuth implementation.

def login():
	CONSUMER_KEY = ''
	CONSUMER_SECRET = ''
	OAUTH_TOKEN = ''
	OAUTH_TOKEN_SECRET = ''

	auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
	                           CONSUMER_KEY, CONSUMER_SECRET)
	
	twitter_api = twitter.Twitter(auth=auth)
	return twitter_api
