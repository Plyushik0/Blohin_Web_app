from flask import Flask, request, render_template, redirect, make_response
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'users.db'

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('CREATE TABLE users (username TEXT, password TEXT)')
        conn.commit()
        conn.close()
init_db()

@app.route('/')
def root():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # УЯЗВИМОСТЬ: SQL-инъекция!
        c.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
        user = c.fetchone()
        conn.close()
        if user:
            resp = make_response(redirect('/welcome'))
            resp.set_cookie('user', username)
            return resp
        else:
            return "Ошибка входа"
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    username = request.cookies.get('user')
    if not username:
        return redirect('/login')
    return render_template('welcome.html', username=username)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)