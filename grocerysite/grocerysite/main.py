from app import app
from flask import flash, session, render_template, request, redirect
from werkzeug import generate_password_hash, check_password_hash

@app.route('/')
def index():
  if 'email' in session:
    username = session['email']
    return 'Logged in as ' + username + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>"
  return "You are not logged in <br><a href = '/login'></b>" + "click here to login</b></a>"

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/submit', methods=['POST'])
def login_submit():
  _username = request.form['username']
  if _username and request.method == 'POST':
    conn = None
    try:
      conn = sqlite3.connect(r"../db.sqlite3")
      cur = conn.cursor()
      sql = "select username from auth_user")
      sql_where = (_username,)
      cur.execute(sql, sql_where)
      row = cur.fetchone()
      if row:
        session['email'] = row[1]
        cur.close()
        conn.close()
        return redirect('/')
      else:
        flash('Invalid email!')
        return redirect('/login')

@app.route('/logout')
def logout():
  session.pop('email', None)
  return redirect('/')

if __name__ == "__maiun__":
  app.run()
