from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import config

app = Flask(__name__)
app.secret_key = 'your secret key'

def check_user(username, password):
    conn = psycopg2.connect(
        host=config.pg_host,
        database=config.pg_database,
        user=config.pg_user,
        password=config.pg_password
    )
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
    user = cur.fetchone()
    conn.close()

    if user:
        return True
    else:
        return False

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if check_user(username, password):
        flash('Logged in successfully!', 'success')
        return redirect(url_for('home'))
    else:
        flash('Invalid credentials. Please try again.', 'error')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app
