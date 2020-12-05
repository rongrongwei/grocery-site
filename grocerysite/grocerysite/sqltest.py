import sqlite3
import hashlib

try:
  conn = sqlite3.connect(r"../db.sqlite3")
except Error as e:
    print(e)

cur = conn.cursor()

cur.execute("select username, password from auth_user")

username = "admin"
for row in cur:
    print(row[0] + row[1]);

#password = "password"

#hash = hashlib.sha256(password.encode())

#print(password + ": sha256$" + hash.hexdigest())



