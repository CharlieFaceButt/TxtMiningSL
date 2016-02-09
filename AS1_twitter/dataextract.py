import json
import os
from collections import Counter

path = './tweet_stream'
files = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path,i)) and \
         'captured_tweets_' in i]
print str(len(files)) + " files loaded"

# Tweet amount
tweetAmount = 0
# Total number of words in collection, and it is also used to 
# calculate average number of words per tweet
totalWords = 0

counter = Counter()

for infile in files:
	with open(os.path.join(path,infile)) as json_file:
		data = json.load(json_file)
		tweetAmount += len(data)
		for key, value in data.items():
			words = value.split(" ")
			totalWords += len(words)
			for word in words:
				counter[word] += 1
print str(tweetAmount) + " tweets loaded"
print "Total number of words: " + str(totalWords)
print "Average number of words per tweet: " + str(totalWords / tweetAmount)
uniqueWordAmount = len(counter)
print "Total number of unique words: " + str(uniqueWordAmount)
print "Lexical diversity: " + str(1.000 * uniqueWordAmount / totalWords)
print "most common words: " + str(counter.most_common(50))
