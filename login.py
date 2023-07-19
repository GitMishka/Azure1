from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Manonthemoon123@database-1.cueq5a3aruqx.us-east-2.rds.amazonaws.com/postgres'
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Flask Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# SQLAlchemy User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@login_required
def home():
    return "Welcome!"

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password'
    else:
        return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return 'You are now logged out'

if __name__ == '__main__':
    db.create_all()  # creates the tables
    app.run(debug=True)
