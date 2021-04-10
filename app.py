from flask import Flask, request
import time
from random import randint
import sqlite3
import ast


app = Flask(__name__)
sessions = []


@app.route('/api/createUser', methods=["POST"])
def createUser():
    """
    Requires email, pwd, name, bio #and age
    """
    args = request.get_json()
    # print(args)
    conn = sqlite3.connect('nesamani.db')
    cur = conn.cursor()
    try:
        cur.execute(f"""insert into Users (name, email, pwd, utc, uid) values(?, ?, ?, ?, ?)""",
            (args['name'], args['email'], args['pwd'], time.time(), randint(0, 999999)))
        conn.commit()
        conn.close()
        return {"msg": "Inserted into DB successfully!"}, 201
    except sqlite3.IntegrityError:
        conn.close()
        return {"msg": "Email ID taken!"}, 404


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
        cur.execute(f"select pwd from users where email=?",(args["email"],))
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
        cur.execute(f"select * from users where email=?", (args["email"],))
        details = cur.fetchone()
        # print(pwd)
        if details[0]:
            if args['email'] not in sessions:
                data = {
                    'user_name': details[0],
                    'email': details[1],
                    'joined_on': time.strftime("%D", time.localtime(details[3])),
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
        utc = time.time()
        try:
            conn = sqlite3.connect('nesamani.db')
            cur = conn.cursor()
            cur.execute(f"""insert into Projects(pid, title, desc, umail, utc) values(?,?,?,?,?)""",
                (pid,
                args['title'],
                args['description'],
                args['email'],
                utc))
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
    try:
        conn = sqlite3.connect('nesamani.db')
        cur = conn.cursor()
        cur.execute('select * from projects')
        data = cur.fetchall()
        '''
        response = {
            "pid": [x[0] for x in data],
            'title': [x[1] for x in data],
            'desc': [x[2] for x in data],
            'umail': [x[3] for x in data],
            'utc': [time.strftime("%D", time.localtime(x[4]) for x in data]
        }
        '''
        r = '{"result":[\n'

        for x in data:
            #print("no erroes here", x[3])
            cur.execute('select name from users where email="{}";'.format(x[3]))
            user_name = cur.fetchall()[0][0]
            #print("username", user_name)
            response = str({
                "idea_id": x[0],
                "title": x[1],
                "description": x[2],
                "user_id": x[3],
                "date": time.strftime("%D", time.localtime(x[4])),
                "user_name": user_name
            })
            r += response + ',\n'
        r += ']}'
        i = r.rindex(',')
        r = r[:i] + r[i+1:]
        conn.close()
        #print(r)
        r = ast.literal_eval(r)
        return r, 200
    except:
        conn.close()
        return {"msg": "ERROR!"}


@app.route('/api/getProject', methods=["GET"])
def getProject():
    """
    Takes pid (project id) as input
    """
    pid = request.get_json()['idea_id']
    try:
        conn = sqlite3.connect('nesamani.db')
        cur = conn.cursor()
        cur.execute(f'select * from projects where pid=?',(pid,))
        x = cur.fetchone()
        cur.execute('select name from users where email="{}";'.format(x[3]))
        user_name = cur.fetchall()[0][0]
        response = {
            "idea_id": x[0],
            'title': x[1],
            'description': x[2],
            'user_id': x[3],
            "user_name": user_name,
            'date': time.strftime("%D", time.localtime(x[4]))
        }
        conn.close()
        return response, 200
    except:
        conn.close()
        return {"msg": "Project not found!"}, 404


@app.route('/api/getUserProject', methods=["GET"])
def getUserProject():
    """
    Takes pid (project id) as input
    """
    umail = request.get_json()['user_id']
    try:
        conn = sqlite3.connect('nesamani.db')
        cur = conn.cursor()
        cur.execute(f'select * from projects where umail=?',(umail,))
        data = cur.fetchall()
        r = '{"result":[\n'

        for x in data:
            #print("no erroes here", x[3])
            cur.execute('select name from users where email="{}";'.format(x[3]))
            user_name = cur.fetchall()[0][0]
            #print("username", user_name)
            response = str({
                "idea_id": x[0],
                "title": x[1],
                "description": x[2],
                "user_id": x[3],
                "date": time.strftime("%D", time.localtime(x[4])),
                "user_name": user_name
            })
            r += response + ',\n'
        r += ']}'
        r = ast.literal_eval(r)
        conn.close()
        return r, 200
    except:
        conn.close()
        return {"msg": "Project not found!"}, 404


@app.route('/api/addTeamMate', methods=['POST'])
def addTeammate():
    """
    umail : Mail of project owner
    omail : mail of person to add, can be element or list
    pid   : project id
    """
    args = request.get_json()
    if args['umail'] not in sessions:
        return {"msg": "user not signed in!"}, 404
    # try:
    if True:
        conn = sqlite3.connect('nesamani.db')
        cur = conn.cursor()
        cur.execute(f'select umail from projects where pid=?', (args["pid"],))
        x = cur.fetchone()
        if not x[0] == args['umail']:
            return {"msg": "You don't have permission!"}, 405
        if type(args['omail']) == list:
            for mail in args['omail']:
                data = cur.execute("select email from users;")
                users = data.fetchall()
                print(users)
                if mail not in users:
                    return {"msg": "user no exist"}, 404
                cur.execute(f'''insert into team (tid, uid, utc) values(?,?,?)''', (args["pid"], mail,time.time()))
                conn.commit()
        elif type(args['omail']) == str:
            data = cur.execute("select email from users;")
            users = data.fetchall()
            for user in users:
                print(user)
                if user[0] == args['omail']:
                    break
            else:
                return {"msg": "user no exist"}, 404

            cur.execute(f"""insert into team (tid, uid, utc) values(?,?,?)""",
                (args["pid"],
                args["omail"],
                time.time()))

    #except:
    #    conn.close()
    #    return {"msg": "Project not found 2!"}, 404



@app.route('/api/getProjectLink', methods=["GET"])
def getProjectLink():
    args = request.get_json()
    try:
        conn = sqlite3.connect('nesamani.db')
        cur = conn.cursor()
        cur.execute(f'select link from link where pid=?',(pid,))
        x = cur.fetchone()
        return {"link": x[0]}, 200
    except:
        conn.close()
        return {"msg": "Link not found!"}, 404


@app.route('/api/postProjectLink', methods=["GET"])
def setProjectLink():
    pid = request.get_json()["pid"]
    try:
        conn = sqlite3.connect('nesamani.db')
        cur = conn.cursor()
        cur.execute(f'select link from link where pid=?',(pid,))
        x = cur.fetchone()
        return {"link": x[0]}, 200
    except:
        conn.close()
        return {"msg": "Link not found!"}, 404

if __name__ == '__main__':
    app.run(debug=True)
