from flask import Flask, render_template, request, session, redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb+srv://muskan:aditi@cluster0-nvyf0.mongodb.net/pms?retryWrites=true&w=majority")
db = client.get_database('pms')
app = Flask(__name__)


@app.route("/")
def home():
    current_user=db.cu
    culist=list(current_user.find())
    if len(culist)!=0:
        user=db.user
        k5=list(user.find({"username":culist[0]["username"]}))
        return render_template('entry.html',k5=k5)
    return render_template('index.html')



@app.route("/login")
def login():
    current_user = db.cu
    culist = list(current_user.find())
    if len(culist) != 0:
        user = db.user
        k5 = list(user.find({"username": culist[0]["username"]}))
        return render_template('entry.html', k5=k5)
    return render_template('login.html',flag=0)


@app.route("/register")
def register():
    current_user = db.cu
    culist = list(current_user.find())
    if len(culist) != 0:
        user = db.user
        k5 = list(user.find({"username": culist[0]["username"]}))
        return render_template('entry.html', k5=k5)
    return render_template('register.html',flag=0,h='')


@app.route("/registered", methods=['GET', 'POST'])
def registered():
    if request.method == 'POST':
        username = request.form.get('user')
        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('mob')
        address = request.form.get('add')
        password = request.form.get('password')
        qq = db.user
        k6 = list(qq.find({'username':username}))
        if len(k6)!=0:
            h='Username Exist'
            return render_template('register.html', flag=0, f=1, h=h)
        dic = {"name": name, "username": username, "password": password, "mob": mobile, "email": email,
               "address": address}
        qq.insert_one(dic)

    return render_template('register.html',flag=1,h='')


@app.route("/logout")
def logout():
    te = db.cu
    ju = list(te.find())
    r = db.record
    gh = {"username": ju[0]["username"], "logout": "b"}
    ty = list(r.find(gh))
    dr = {"username": ju[0]["username"], "logout": "b", "login": ty[0]["login"]}
    dt = datetime.now()
    dd = {"username": ju[0]["username"], "logout": dt, "login": ty[0]["login"]}
    r.update_one(dr, {'$set': dd})
    te.delete_many({})
    return redirect('/login')

@app.route("/entry", methods=['GET', 'POST'])
def entry():
    current_user = db.cu
    if request.method == 'POST':
        username = request.form.get('userid')
        password = request.form.get('password')
        qw = db.user
        r=db.record
        dt=datetime.now()
        k5 = list(qw.find({"username": username}))
        if (len(k5) != 0 and password == k5[0]["password"]):
            de={'username':username}
            dic_dtt={'username':username,'logout':'b','login':dt}
            r.insert_one(dic_dtt)
            current_user.insert_one(de)
            return render_template('entry.html', k5=k5)
        else:
            return render_template('login.html',flag=1)
    k7 = list(current_user.find())
    users = k7[0]['username']
    qs = db.user
    k6 = list(qs.find({'username': users}))

    return render_template('entry.html',k5=k6)

@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        no = request.form.get('number')
        name = request.form.get('name')
        dt = datetime.now()
        qww = db.data
        dd = {"name": name, "number": no, "entry": dt, "exit": "b"}
        qww.insert_one(dd)
        return render_template('add.html',flag=1)

    return render_template('add.html',flag=0)


@app.route("/exit", methods=['GET', 'POST'])
def exitt():
    if request.method == 'POST':
        no = request.form.get('number')
        dr = {"number": no, "exit": "b"}
        dt = datetime.now()
        dd = {"number": no, "exit": dt}
        qww = db.data
        qww.update_one(dr, {'$set': dd})
        return render_template('exit.html', flag=1)

    return render_template('exit.html', flag=0)
@app.route("/history", methods=['GET', 'POST'])
def history():
    if request.method == 'POST':
        no = request.form.get('number')
        qww = db.data
        k5 = list(qww.find({"number": no}))
        if len(k5) != 0:
            return render_template('hist.html', k5=k5)
        return render_template('history.html', flag=1)
    return render_template('history.html', flag=0)

@app.route("/loginh")
def historylogin():
    gt = db.record
    k5 = list(gt.find())
    return render_template('loginhist.html', k5=k5)
