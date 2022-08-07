from flask import Flask, make_response, redirect, request, render_template, url_for
from krypton.auth.users.userModel import standardUser
from krypton.auth.users.bases import UserError
from functools import wraps
import json
import krypton

# krypton.configs.SQLDefaultUserDBpath = "mssql+pyodbc://localhost/userDB?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=no"
krypton.configs.HOST_NAME = 'localhost'
krypton.configs.ORIGIN = 'http://localhost:5000'

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

## FIDO Stuff

@app.route('/getFidoLogin', methods=['POST'])
def getFido():
    email = request.get_json()["email"]
    try:
        user = standardUser(email)
    except UserError:
        resp = make_response('{"error": "Access Denied"}')
        return resp
    options = user.getFIDOOptions()
    resp = make_response(options)
    return resp

@app.route('/FIDOLogin', methods=["GET"])
@get_user
def fidoLogin(current_user):
    return render_template("FIDOLogin.html", current_user=current_user)

@app.route('/FIDOLogin', methods=["POST"])
def fidoLogin_post():
    fido = json.dumps(request.get_json())
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    try:
        user = standardUser(email)
        token = user.login(password, fido=fido)
        if token is False:
            raise UserError("Token is False")
    except UserError:
         return render_template('login.html', msg="Error. Please check your credentials.", current_user = standardUser(None))
    resp = make_response('{"username":"'+email+'", "_kryptonAuthToken":"'+token+'"}')
    resp.set_cookie('username', email)
    resp.set_cookie('_kryptonAuthToken', token)
    return resp

@app.route('/fido')
@login_required
def fido(current_user):
    return render_template('fido.html', current_user = current_user)

@app.route('/fidoReg')
@login_required
def fidoReg(current_user:standardUser):
    options = current_user.beginFIDOSetup()
    return options

@app.route('/fidoFinishReg', methods=['POST'])
@get_user
def fidoRegFinish(current_user:standardUser):
    current_user.completeFIDOSetup(json.dumps(request.get_json()))
    return make_response(redirect(url_for('profile')))


## SignUp/Login/Profile

@app.route('/login')
@get_user
def login(current_user):
    return render_template('login.html', current_user = current_user)

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = standardUser(email)
        token = user.login(password)
    except UserError:
        try:
            if user.FIDORequired is True:
                return make_response(redirect(url_for("fidoLogin", password=password, username=email)))
        except UnboundLocalError:
            pass
        return render_template('login.html', msg="Error. Please check your credentials.", current_user = standardUser(None))
    resp = make_response(redirect(url_for('profile')))
    resp.set_cookie('username', email)
    resp.set_cookie('_kryptonAuthToken', token)
    return resp


@app.route('/signup', methods=["GET"])
@get_user
def signup(current_user):
    return render_template("signup.html", current_user= current_user)

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = standardUser(None)
    try:
        token = user.saveNewUser(email, password)
    except:
        return render_template('signup.html', msg="Error. Please check your credentials.", current_user=standardUser(None))
    user.setData("name", name)
    resp = make_response(redirect(url_for('profile')))
    resp.set_cookie('username', email)
    resp.set_cookie('_kryptonAuthToken', token)
    return resp

@app.route('/logout')
@login_required
def logout(current_user:standardUser):
    current_user.logout()
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie("_kryptonAuthToken", max_age=0)
    return resp

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
