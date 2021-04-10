import requests

BASE = 'http://127.0.0.1:5000/api'

# Test User Endpoint
# 1. Create user
response = requests.post(BASE+'/createUser', json={
    "user_name": "Sakthi",
    "pwd": "CloudLead",
    "user_id": "realaddress@fake.com",
    })
print(response.json())

# 2. Create user with existing mail
response = requests.post(BASE+'/createUser', json={
    "user_name": "Sakthi",
    "pwd": "CloudLead",
    "user_id": "realaddress@fake.com",
    })
print(response.json())

# 3. Login user with right deets
response = requests.get(BASE+'/loginUser', json={
    "pwd": "CloudLead",
    "user_id": "realaddress@fake.com",
    })
print(response.json())

# 4. Login user with wrong deets
response = requests.get(BASE+'/loginUser', json={
    "pwd": "wrongpassword",
    "user_id": "realaddress@fake.com",
    })
print(response.json())

# 5. Logout user
response = requests.get(BASE+'/logoutUser', json={
    "user_id": "realaddress@fake.com",
    })
print(response.json())

# 5. Get user deets that exists
response = requests.get(BASE+'/getUser', json={
    "user_id": "realaddress@fake.com",
    })
print(response.json())

# 6. Get user deets that dont exists
response = requests.get(BASE+'/getUser', json={
    "user_id": "notanaddress@fake.com",
    })
print(response.json())
