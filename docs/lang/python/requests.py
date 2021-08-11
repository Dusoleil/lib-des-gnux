import requests
import json

# GET
r = requests.get("https://httpbin.org/get?a=b&c=d")
print(r.headers)
print(r.text)

# POST
r = requests.post("https://httpbin.org/post",
        data={'a': 'b', 'c': 'd'})

# POST JSON
r = requests.post("https://httpbin.org/post",
        json={'a': 'b', 'c': 'd'})
print(r.json())

# Request headers
r = requests.get("https://httpbin.org/get",
        headers={'DNT': '1'}) # Do not track

# Session (any cookies obtained will be saved/sent with follow-up requests)
s = requests.Session()
r = s.post("...",
        data={'username': '...', "password": '...'})
r = s.get(".../my_user_data")
