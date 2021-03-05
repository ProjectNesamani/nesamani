import requests

BASE = 'http://127.0.0.1:5000/api'

# Test Project Endpoint
# 1. Create Project with existing user who isn't logged in
response = requests.post(BASE+'/createProject', json={
    "title": "A Project",
    "desc": "This project will do good things for everyone",
    "email": "realaddress@fake.com",
    })
print(response.json())
# Log user in
response = requests.get(BASE+'/loginUser', json={
    "pwd": "CloudLead",
    "email": "realaddress@fake.com",
    })
print(response.json())
# 2. Create Project with existing user who is logged in
response = requests.post(BASE+'/createProject', json={
    "title": "A Project",
    "desc": "This project will do good things for everyone",
    "email": "realaddress@fake.com",
    })
print(response.json())
