from __future__ import unicode_literals

from django.db import models
from collections import Counter
from django.utils import timezone

class QueryRecord(models.Model):
	query_text = models.CharField(max_length=100)
	query_media = models.CharField(max_length=20, default='twitter')
	query_time = models.DateTimeField()
	def __str__(self):
		return self.query_text

class QueryResult(models.Model):
	result_pos = models.IntegerField(default=0)
	result_neu = models.IntegerField(default=0)
	result_neg = models.IntegerField(default=0)
	result_query = models.ForeignKey(QueryRecord, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.result_pos) + "/" + str(self.result_neu) + "/" + str(self.result_neg)

class MostCommonQuery(models.Model):
	most_common = models.CharField(max_length=200, default='default')
	drift_time = models.DateTimeField(null=True)
	def __str__(self):
		return str(self.most_common)
	@staticmethod
	def newLog():
		counter = Counter()
		dataset = QueryRecord.objects.all()
		for data in dataset:
			counter[data.query_text] += 1
		mcq = MostCommonQuery(most_common=counter.most_common(5),drift_time=timezone.now())
		mcq.save()
	@staticmethod
	def getLog():
		dataset = MostCommonQuery.objects.all()
		return dataset[len(dataset) - 1]