import requests

print(requests.get('http://127.0.0.1/api/jobs').json())
print(requests.get('http://127.0.0.1/api/jobs/1').json())
print(requests.get('http://127.0.0.1/api/jobs/775').json())
print(requests.get('http://127.0.0.1/api/jobs/redtggfh').json())
