from flask import Flask, request, redirect, make_response, render_template_string
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'users.db'


if not os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')
    conn.commit()
    conn.close()


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
    return render_template_string('''
        <h2>Регистрация</h2>
        <form method="post">
            Логин: <input name="username"><br>
            Пароль: <input name="password" type="password"><br>
            <input type="submit" value="Зарегистрироваться">
        </form>
    ''')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
        user = c.fetchone()
        conn.close()
        if user:
            resp = make_response(redirect('/welcome'))
            resp.set_cookie('username', username)
            return resp
        else:
            return 'Неверный логин или пароль'
    return render_template_string('''
        <h2>Авторизация</h2>
        <form method="post">
            Логин: <input name="username"><br>
            Пароль: <input name="password" type="password"><br>
            <input type="submit" value="Войти">
        </form>
    ''')


@app.route('/welcome')
def welcome():
    username = request.cookies.get('username')
    if not username:
        return redirect('/login')
    return f'Привет, {username}'


@app.route('/')
def index():
    return redirect('/register')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
