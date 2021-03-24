from flask import Flask,render_template,request,url_for,redirect,session
from pymongo import *
from datetime import datetime
from random import *
from flask_mail import Mail,Message
app=Flask(__name__)

app.secret_key = '12346554'


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'jbg9*******597@gmail.com'
app.config['MAIL_PASSWORD'] = '9********'


app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)





@app.route("/")
def index():
    return render_template('signup.html')

@app.route("/register",methods=['GET'])
def register():
    name=request.args.get("username")
    email = request.args.get("email")
    mobile = request.args.get("mobile")
    deg = request.args.get("deg")
    con = MongoClient("mongodb+srv://********")
    db = con ['user']
    col=db['reg']
    now = datetime.now()
    ct = now.strftime("%H:%M:%S")
    s = '09:00:00'
    e = '22:00:00'
    if (ct >= s) and (ct <= e):
        if (name != '') and (email != '') and (mobile != '') and (deg != ''):
            for l in col.find({"email": email}):
                return render_template("signup.html", msg="Email id is already exist")
            else:
                col.insert_one({"name": name, "email": email, "mobile": mobile, "degree": deg})
                return render_template("login.html", msg="Registration is done successful")
        else:
            render_template("signup.html", msg="The field is empty")
    else:
        return render_template("signup.html", msg="Time is out")



@app.route("/login",methods=['GET'])
def login():
    email = request.args.get("email")
    password = request.args.get("password")
    con = MongoClient("mongodb+srv://")
    db = con['user']
    col = db['reg']
    now = datetime.now()
    ct = now.strftime("%H:%M:%S")
    s = '09:00:00'
    e = '22:00:00'
    if (ct>=s) and (ct<=e):

        for i in col.find({"email": email}):
            print(email)
            if str(session['password']) == password:
                return redirect(url_for("cards"))
                session.clear()


            else:
                return render_template('login.html', msg="Password is incorrect")
        else:
            return render_template("login.html", msg="unauthorized user")
    else:
        return render_template("login.html",msg="time is out")





@app.route('/signin')
def signin():
    return render_template("login.html")


@app.route('/verify', methods=['GET'])
def verify():
    email = request.args.get('email')
    msg = Message(subject='OTP', sender='jbg9787*******@gmail.com', recipients=[email])
    otp = randint(100000, 999999)

    msg.body = str(otp)
    mail.send(msg)
    session['password'] = str(otp)
    return render_template('login.html')




#
@app.route("/cards")
def cards():
    con = MongoClient("mongodb+srv://")
    db = con['collegeweb']
    col = db['colleges']
    res=[]
    for i in col.find():
        res.append(i)
    return render_template("cards.html",data=res)


# @app.route("/search",methods=['GET'])
# def ver():
#     search=request.args.get('search')
#     con = MongoClient("mongodb+srv://")
#     db = con['user']
#     col = db['colleges']
#     r=[]
#     for k in col.find({'clg name':search}):
#         r.append(k)
#         return render_template('c2.html',res=r)
#     else:
#         return render_template("c2.html", msg='Type College Name in Caps')
app.run(debug=True)
