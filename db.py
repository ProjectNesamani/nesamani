'''
Create Tables

1. Users
    name, email, pwd, utc, age

2. Projects
    pid, title, desc, umail, utc, tid

3. Tags
    id, tag

4. Ratings
    pid, uid, rating, feedback, utc

5. Team
    name, tagline, uid, tid, utc

6. Links
    pid, link, utc
'''
import sqlite3
from configparser import ConfigParser

config = ConfigParser()
config.read('/app/config.ini')
conf = config['DATABASE']
print()
def createUsers():
    """
    Function to create the Users table
    """
    conn = sqlite3.connect(conf['path'])
    cur = conn.cursor()
    # Add dp as string later
    cur.execute('''Create Table If Not Exists Users(\
        name varchar(20) not null,\
        email varchar(32) unique not null primary key,\
        pwd varchar(32) not null,\
        utc timestamp not null,\
        uid integer
    );''')
    conn.commit()
    conn.close()


def createProjects():
    """
    Function to create the Projects table
    """
    conn = sqlite3.connect(conf['path'])
    cur = conn.cursor()
    # Add dp as string later
    cur.execute('''Create Table If Not Exists Projects(\
        pid Primary Key,\
        title varchar(100) not null,\
        desc varchar(500) not null,\
        umail integer not null,\
        utc timestamp not null\
    );''')
    conn.commit()
    conn.close()


def createTags():
    """
    Function to create the Tags table
    """
    conn = sqlite3.connect(conf['path'])
    cur = conn.cursor()
    # Add dp as string later
    cur.execute('''Create Table If Not Exists Tags(\
        pid integer,\
        tag varchar(32) not null\
    );''')
    conn.commit()
    conn.close()


def createRatings():
    """
    Function to create the Ratings table
    """
    conn = sqlite3.connect(conf['path'])
    cur = conn.cursor()
    # Add dp as string later
    cur.execute('''Create Table If Not Exists Ratings(\
        pid integer,\
        uid integer,\
        rating real not null,\
        feedback varchar(500) not null,\
        utc timestamp\
    );''')
    conn.commit()
    conn.close()


def createTeam():
    """
    Function to create the Team table
    """
    conn = sqlite3.connect(conf['path'])
    cur = conn.cursor()
    # Add dp as string later
    # name varchar(32) not null,\
    # desc varchar(250) unique not null,\
    cur.execute('''Create Table If Not Exists Team(\
        pid integer Primary Key,\
        umail varchar(32),\
        utc timestamp not null\
    );''')
    conn.commit()
    conn.close()


def createLinks():
    """
    Function to create the Links table
    """
    conn = sqlite3.connect(conf['path'])
    cur = conn.cursor()
    # Add dp as string later
    # name varchar(32) not null,\
    # desc varchar(250) unique not null,\
    cur.execute('''Create Table If Not Exists Link(\
        pid integer Primary Key,\
        link varchar(50),\
        utc timestamp not null\
    );''')
    conn.commit()
    conn.close()


def createAll():
    """
    Function to create the All table
    """
    createUsers()
    createProjects()
    createTags()
    createRatings()
    createTeam()
    createLinks()


if __name__ == '__main__':
    createAll()
