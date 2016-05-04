import json
from auth import weibo_login

weibo_api = weibo_login()
weibo_api.statuses__public_timeline(count=100)
statuses = public_timeline['statuses']
print json.dumps(statuses, indent = 4)
