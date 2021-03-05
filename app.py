from flask import Flask, request
from time import time
from random import randint
import sqlite3
app = Flask(__name__)
sessions = []


@app.route('/api/createUser', methods=["POST"])
def createUser():
    """
    Requires email, pwd, name, bio and age
    """
    args = request.get_json()
    # print(args)
    conn = sqlite3.connect('nesamani.db')
    cur = conn.cursor()
    try:
        cur.execute(f"""insert into Users (name, email, pwd, utc, age) values(\
            '{args['name']}','{args['email']}','{args['pwd']}',{time()},{args['age']}\
        );""")
        conn.commit()
        conn.close()
        return {"message": "Inserted into DB successfully!"}, 201
    except sqlite3.IntegrityError:
        conn.close()
        return {'msg': 'Email ID taken!'}, 404


@app.route('/api/loginUser', methods=['GET'])
def loginUser():
    """
    Requires email, pwd
    """
    args = request.get_json()
    # print(args)
    conn = sqlite3.connect('nesamani.db')
    cur = conn.cursor()
    try:
        cur.execute(f'select pwd from users where email="{args["email"]}";')
        pwd = cur.fetchone()
        # print(pwd)
        if pwd[0] == args['pwd']:
            if args['email'] not in sessions:
                sessions.append(args['email'])
                return {"msg": "Login successful!"}, 200
            else:
                return {"msg": "Already logged in!"}, 404
        else:
            return {"msg": "Login not successful!"}, 404
    except sqlite3.IntegrityError:
        conn.close()
        return {'msg': 'Email ID taken!'}, 404


@app.route('/api/getUser', methods=['GET'])
def getUser():
    """
    Requires email
    """
    args = request.get_json()
    # print(args)
    conn = sqlite3.connect('nesamani.db')
    cur = conn.cursor()
    try:
        cur.execute(f'select * from users where email="{args["email"]}";')
        details = cur.fetchone()
        # print(pwd)
        if details[0]:
            if args['email'] not in sessions:
                data = {
                    'name': details[0],
                    'email': details[1],
                    'utc': details[3],
                    'age': details[4]
                }
                return data, 200
        else:
            return {"msg": "User not found!"}, 404
    except TypeError:
        return {"msg": "User not found!"}, 404
    except sqlite3.IntegrityError:
        conn.close()
        return {'msg': 'Error!'}, 404


@app.route('/api/updateUser', methods=['PUT'])
def updateUser():
    """
    Updates name and bio
    Do it later
    """
    # args = request.get_json()
    conn = sqlite3.connect('nesamani.db')
    # cur = conn.cursor()
    conn.close()
    return {"msg": "Not implemented yet"}


@app.route('/api/deleteUser', methods=['DELETE'])
def deleteUser():
    """
    Requires email
    Do it later
    """
    args = request.get_json()
    if args['email'] in sessions:
        return {"msg": "Not implemented yet"}
    conn = sqlite3.connect('nesamani.db')
    # cur = conn.cursor()
    conn.close()
    return {"msg": "Not implemented yet"}


@app.route('/api/logoutUser', methods=['GET'])
def logoutUser():
    """
    Requires email
    """
    args = request.get_json()
    if args['email'] in sessions:
        sessions.remove(args['email'])
        return {"msg": "Logout successful!"}, 200
    return {"msg": "User not logged in!"}, 404


@app.route('/api/createProject', methods=['POST'])
def createProject():
    """
    Requires email, title, description to create project
    """
    args = request.get_json()
    if args['email'] in sessions:
        pid = randint(0, 9999999)
        utc = time()
        try:
            conn = sqlite3.connect('nesamani.db')
            cur = conn.cursor()
            cur.execute(f"""insert into Projects(pid, title, desc, umail, utc) values(\
                {pid},\
                '{args['title']}',\
                '{args['desc']}',\
                '{args['email']}',\
                {utc}
            );""")
            conn.commit()
            conn.close()
            return {"msg": "Project Created Successfully!"}, 201
        except sqlite3.IntegrityError:
            conn.close()
            return {"msg": "Error!"}, 404
    return {"msg": "User not logged in!"}, 404

@app.route('/api/feed', methods=["GET"])
def getFeed():
    """
    Get all projects for feed
    """
    args = request.get_json()
    try:
        conn = sqlite3.connect('nesamani.db')
        cur = conn.cursor()
        cur.execute('select * from projects')
        cur.fetchall()
        
    except:
        return {"msg": "ERROR!"}

if __name__ == '__main__':
    app.run(debug=True)
