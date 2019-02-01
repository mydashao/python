import requests
s= requests.Session()
s.get('http://httpbin.org/cookies/set/number/12345')
r= s.get('http://httpbin.org/cookies')
print(r.text)