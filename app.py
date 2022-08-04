from flask import Flask, make_response, redirect, request, render_template, url_for
from krypton.auth.users.userModel import standardUser
from functools import wraps

app = Flask(__name__)

def login_required(func):
    current_user:standardUser
    @wraps(func)
    def inner():
        global current_user
        try:
            username = request.cookies.get('username')
            token = request.cookies.get('_kryptonAuthToken')
            current_user = standardUser(username)
            current_user.restoreSession(token)
        except:
            return render_template("index.html")
        return func()
    return inner

def get_user(func):
    current_user:standardUser
    @wraps(func)
    def inner():
        global current_user
        try:
            username = request.cookies.get('username')
            token = request.cookies.get('_kryptonAuthToken')
            current_user = standardUser(username)
            current_user.restoreSession(token)
            return func()
        except:
            return func()
    return inner

@app.route('/login')
@get_user
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = standardUser(email)
    token = user.login(password)
    resp = make_response(redirect(url_for('main.profile')))
    resp.set_cookie('username', email)
    resp.set_cookie('_kryptonAuthToken', token)
    return resp

@app.route('/signup')
@get_user
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = standardUser(None)
    token = user.saveNewUser(email, password)
    user.setData("name", name)
    resp = make_response(redirect(url_for('main.profile')))
    resp.set_cookie('username', email)
    resp.set_cookie('_kryptonAuthToken', token)
    return resp

@app.route('/logout')
@login_required
def logout():
    current_user.logout()
    return redirect(url_for('main.index'))

@app.route('/')
@get_user
def index():
    return render_template('index.html', current_user = current_user)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.userName)
