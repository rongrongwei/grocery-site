#!/usr/bin/env python3

import sqlite3

def create_connection(db_file):
  conn = None

  try:
    conn = sqlite3.connect(db_file)
  except Error as e:
    print(e)

  return conn


def select_user(conn):
  cur = conn.cursor()
  cur.execute("select username from auth_user")

  rows = cur.fetchall()

  for row in rows:
    user = row

  return user


if __name__ == "__main__":
  
  database = r"../db.sqlite3"

  conn = create_connection(database)
  with conn:
    print("Printing users:")
    user = select_user(conn)
    print(user)
    
