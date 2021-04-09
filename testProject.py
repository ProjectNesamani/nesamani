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

# 3. Get projects for feed
response = requests.get(BASE+'/feed')
print(response.json())
# 4. Get project that exists
response = requests.get(BASE+'/getProject', json={
    "pid": 7645074
    })
print(response.json())
# 5. Get project that dont exists
response = requests.get(BASE+'/getProject', json={
    "pid": 69
    })
print(response.json())
# 6. Add teammate to project that exists

requests.post(BASE+'/createUser', json={
    "name": "Agastya",
    "pwd": "CloudLead",
    "email": "cloud@fake.com",
    "age": 21
    })

response = requests.post(BASE+'/addTeamMate', json={
    "pid": 217303,
    "umail": "realaddress@fake.com",
    "omail": "cloud@fake.com"
})
print(response.json())
