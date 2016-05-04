from django.contrib import admin

from .models import QueryRecord, MostCommonQuery, QueryResult

admin.site.register(QueryRecord)
admin.site.register(MostCommonQuery)
admin.site.register(QueryResult)