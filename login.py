from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import config

app = Flask(__name__)
app.secret_key = 'secretkey' 

def check_user(username, password):
    conn = psycopg2.connect(
        host=config.pg_host,
        database=config.pg_database,
        user=config.pg_user,
        password=config.pg_password
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password,))
    user = cur.fetchone()
    conn.close()

    if user:
        return True
    else:
        return False

@app.route('/', methods=['GET', 'POST'])
def home():
    error = None
    if request.method == 'POST':
        if check_user(request.form['username'], request.form['password']):
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            error = 'Invalid credentials. Please try again.'
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
