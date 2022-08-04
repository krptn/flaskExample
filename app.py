from flask import Flask, make_response, redirect, request, render_template, url_for
from krypton.auth.users.userModel import standardUser
from krypton.auth.users.bases import UserError
from functools import wraps

app = Flask(__name__)

def login_required(func):
    @wraps(func)
    def inner():
        try:
            username = request.cookies.get('username')
            token = request.cookies.get('_kryptonAuthToken')
            current_user = standardUser(username)
            current_user.restoreSession(token)
        except UserError:
            return make_response(redirect(url_for('index')))
        return func(current_user)
    return inner

def get_user(func):
    @wraps(func)
    def inner():
        try:
            username = request.cookies.get('username')
            token = request.cookies.get('_kryptonAuthToken')
            current_user = standardUser(username)
            current_user.restoreSession(token)
            return func(current_user)
        except UserError:
            return func(standardUser(None))
    return inner

@app.route('/login')
@get_user
def login(current_user):
    return render_template('login.html', current_user = current_user)

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = standardUser(email)
    token = user.login(password)
    resp = make_response(redirect(url_for('profile')))
    resp.set_cookie('username', email)
    resp.set_cookie('_kryptonAuthToken', token)
    return resp

@app.route('/signup')
@get_user
def signup(current_user):
    return render_template('signup.html', current_user = current_user)

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = standardUser(None)
    token = user.saveNewUser(email, password)
    user.setData("name", name)
    resp = make_response(redirect(url_for('profile')))
    resp.set_cookie('username', email)
    resp.set_cookie('_kryptonAuthToken', token)
    return resp

@app.route('/logout')
@login_required
def logout(current_user:standardUser):
    current_user.logout()
    return redirect(url_for('index'))

@app.route('/index')
@get_user
def index(current_user):
    return render_template('index.html', current_user = current_user)

@app.route('/')
def home():
    return make_response(redirect(url_for('index')))

@app.route('/profile')
@login_required
def profile(current_user):
    return render_template('profile.html', name=current_user.userName, current_user = current_user)
