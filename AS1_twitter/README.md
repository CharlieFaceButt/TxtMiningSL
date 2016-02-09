# Mining twitter

Interest topic is set "Virtual Reality".

To extract tweets using twitter streaming API, run:

<pre><code> python twitter_stream.py </code></pre>

This code will save 100 tweets each time, and put them in folder "tweet_stream".

Then calculate basic statistics using the data just retrieved, run:

<pre><code> python dataextract.py </code></pre>

The code will calculate:

* Total number of tweets collected
* Total number of words in this collection
* Average number of words per tweet
* Total number of unique words in this collection
* Lexical diversity
* Most common words and their counts in this collection

There are already example data in the tweet_stream folder, the code can run directly.