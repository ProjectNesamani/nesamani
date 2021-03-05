# -----------------------------------------------
'''
Implement All APIs here
'''
# -----------------------------------------------
import sqlite3
from flask import request
from app import app
from time import time
# -----------------------------------------------
'''
APIs to
- Create User
- Login User
- Get User details
- Set User details
- Delete User
'''


@app.route('/api/createUser', methods=["POST"])
def createUser():
    """
    Requires email, pwd, name, bio and age
    """
    args = request.get_json()
    print(args)
    conn = sqlite3.connect('nesamani.db')
    cur = conn.cursor()
    try:
        cur.execute(f"insert into Users (name, email, pwd, utc, age) values('{args['name']}','{args['email']}','{args['pwd']}',{time()},{args['age']});")
        conn.commit()
        conn.close()
        return {"message": "Inserted into DB successfully!"}, 201
    except sqlite3.IntegrityError as e:
        print(e)
        conn.close()
        return {'msg': 'Email ID taken!'}, 404

@app.route('/api/loginUser', methods=['GET'])
def loginUser():
    pass


@app.route('/api/getUser', methods=['GET'])
def getUser():
    pass


@app.route('/api/updateUser', methods=['PUT'])
def updateUser():
    pass


@app.route('/api/deleteUser', methods=['DELETE'])
def deleteUser():
    pass
# -----------------------------------------------
