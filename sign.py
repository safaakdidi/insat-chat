import hashlib

import sqlite3 as sq
from user import User

from getpass import getpass
from hashlib import *

# conn = sq.connect("Ma_base.dbs")
# c = conn.cursor()
# # c.execute("DROP TABLE User")
# c.execute("""create table if not exists User(
#     id integer primary key autoincrement,
#     num_cart text,
#     nom text,
#     prenom text,
#     pseudo text,
#     email text,
#     password text,
#     certPath text,
#     keyPath text,
#     is_connected boolean default 0
#     )""")
# conn.commit()
# conn.close()
def db_conn():
    conn = sq.connect("Ma_base.dbs")
    c = conn.cursor()
    # c.execute("""create table if not exists User(
    # id integer primary key autoincrement,
    # num_cart text,
    # nom text,
    # prenom text,
    # pseudo text,
    # email text,
    # password text,
    # certPath text,
    # keyPath text,
    #  is_connected boolean default 0
    # )""")
    return conn, c



def signUp(num_cart, nom, prenom, pseudo, email, password,certPath,keyPath):
    conn, c = db_conn()
    c.execute("""insert into User(num_cart,nom,prenom,pseudo,email,password,certPath,keyPath) values(?,?,?,?,?,?,?,?)""",(num_cart,nom,prenom,pseudo,email,hashlib.sha256(password.encode()).hexdigest(), certPath, keyPath))
    c.execute("""select * from User""")
    items = c.fetchall()
    for item in items:
        print(item)

    conn.commit()
    conn.close()


def signIn(email, pwd):
    conn, c = db_conn()
    c.execute("""select * from User where email=? and password=?""",(email,hashlib.sha256(pwd.encode()).hexdigest()))
    items = c.fetchall()
    for item in items:
        print(item)
    conn.commit()
    conn.close()
    if items:
        return items[0]
    else:
      return None

def getUserById(id):
    conn, c = db_conn()
    c.execute("""select * from User where id=?""", (id,))
    item = c.fetchone()

    print(item)
    conn.commit()
    conn.close()
    if item:
        return User(*item)
    else:
        return None
def getUserByEmail(email):
    conn, c = db_conn()
    c.execute("""select * from User where email=?""", (email,))
    item = c.fetchone()

    print(item)
    conn.commit()
    conn.close()
    if item:
        print(User(*item))
        return User(*item)
    else:
        return None
def connecter(id):
    conn, c = db_conn()
    c.execute("""update User set is_connected=1  where id=?""", (id,))
    conn.commit()
    conn.close()
def deconnecter(id):
    conn, c = db_conn()
    c.execute("""update User set is_connected=0  where id=?""", (id,))
    conn.commit()
    conn.close()

def getConnectedUsers():
    conn, c = db_conn()
    c.execute("""select * from User where is_connected=1""", )
    items = c.fetchall()


    conn.commit()
    conn.close()

    return items


# signUp("1245", "safouuuuuu", "med", "saff", "safa1@gmail.com", "****",'hgjh','jhvjmb')
# connecter(1)
# nom=getUserById(1)
# w=signIn("safa1@gmail.com", "****")
# nom=getUserById(w)
# print(type(nom))
#getUserByEmail('emna@gmail.com')
# signUp('789','pirate','ben pirate','piratouu','pirate@gmail.com','000','build/pirate.cert','build/pirate.key')
