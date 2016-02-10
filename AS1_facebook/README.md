# Homework 1 - Facebook text mining

Course CIS 700, Syracuse University

Interest topic is set "open source"

## Content

Miner.java provide two public static function:

* retriveData(String topic): collect data by indicating topic. Be careful when selecting topic cause either page list in collection, post list of page, or comments of post can be empty set. 
* basicStatisticsOfData(): calculate basic statistics of the collected data from retriveData(). If there is no comment or no post, function will raise error DividedByZero.

The second function will calculate:

* Number of posts collected
* Number of comments collected
* Average number of words per post
* Average number of words per comment
* Lexical diversity of posts
* Lexical diversity of comments

There is a set of example data in data folder, code can run directly using java command.