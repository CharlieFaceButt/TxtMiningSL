import json
import os


def print_score(filepath):
	path = './AS2data'

	with open(path + filepath) as infile:
		# get tweets
		data = json.load(infile)
	# relevant documents retrieved
	rp = 0.0
	# relevant documents
	p = 0.0
	# documents retrived
	r = 0.0

	for obj in data:
		p += obj["P"]
		r += obj["R"]
		rp += obj["RP"]

	print "\n\trecall = " + str(rp/p) + \
		"\n\tprecision = " + str(rp/r) + \
		"\n\tF score = " + str((2 * rp) / (p + r))


print "\n\tFor 50 tweets:"
print_score("/tweets_analysis.json")
print "\n\tFor 50 news sentences:"
print_score("/news_analysis.json")