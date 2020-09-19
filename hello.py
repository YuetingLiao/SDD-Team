#coding=utf-8
import os, json, chardet, pickle, pymysql
#import three_in_one as tio #pyhanlp 出了问题, jvm.dll not found
import pandas as pd
from flask import Flask, redirect, url_for, request, render_template, make_response, session, abort, flash, jsonify
from dotenv import load_dotenv
from werkzeug import secure_filename
app = Flask(__name__)
app.secret_key = "any random string" #这句很重要，否则无法生成session
load_dotenv("test.env")
app.config["JSON_AS_ASCII"]=False #如果不加这句jsonify就会默认把中文字符处理成unicode
#用jsonify处理中文字符非常不稳定，就算配置了这个参数，转换时还是会时常出错
'''
class Config(object):
   DEBUG=True
   JSON_AS_ASCII=False
 
app = Flask(__name__)
 
#从配置对象来加载配置
app.config.from_object(Config)
'''

@app.route('/')
def hello_world():
   return 'Hello World'

@app.route('/success/<name>')
def success(name):
   string = "Welcome  %s%s" #不知道为什么要空两格才能在网站上显示空格
   return string % (name, ", guest!")

@app.route("/start/")
def start():
   return render_template("test.html")

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      if user != "admin":
         abort(401) #返回“无权限”的提示
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

@app.route("/cal/<string:cal>/")
def cal(cal):
   index = cal.find("+")
   if index == -1:
      index = cal.find("-")
   ncal = cal.replace("+", " ")
   ncal = ncal.replace("-", " ")
   [a, b] = ncal.split()
   if cal.count("+") == 1:
      return str(int(a) + int(b)) #一定要转成字符串格式才能成功传到网上
   return str(int(a) - int(b))

@app.route("/hello/<name>/")
def hello_name(name):
   #return "aaaaaaaaaaaaaaaaaaa"
   return render_template("hello.html", name = name)

@app.route("/")
def student():
   return render_template("student.html")

@app.route("/result/", methods = ["POST", "GET"])
def result():
   if request.method=="POST":
      result = request.form
      return render_template("result.html", result=result)

@app.route("/index/")
def index():
   return render_template("index.html")

@app.route("/setcookie/", methods=["POST", "GET"])
def setcookie():
   if request.method == "POST":
      name = request.form["nm"]
   resp = make_response(render_template("readcookie.html"))
   resp.set_cookie("userID", name)
   return resp #不能跳过这一步，如果在直接redirect到getcookie，cookie就不会更新

@app.route("/getcookie/")
def getcookie():
   name = request.cookies.get("userID")
   print(name)
   return "<h1>Welcome "+name+"!</h1>"

@app.route("/page/")
def page():
   if "username" in session:
      username = session["username"]
      return render_template("flash.html", name = username)#莫名其妙第一个空得空两格
   return "You  are not logged in <br><a href='/log'><b>click here to log in</b></a>"

@app.route("/log", methods=["GET", "POST"])
def log():
   error = None
   if request.method=="POST":
      if  request.form["username"] != "admin" and request.form["password"] != "admin":
         error = "Invalid username or password. Please try again!"
      else:
         flash("You were successfully logged in")
         session["username"] = request.form["username"]
         return redirect(url_for("page"))
   return render_template("log.html", error=error)

@app.route("/logout")
def logout():
   session.pop("username", None)
   return redirect(url_for("page"))

@app.route("/upload")
def upload():
   return render_template("upload.html")

@app.route("/up", methods=["GET", "POST"])
def up():
   if request.method=="POST":
      f = request.files["file"]
      path = os.path.dirname(__file__)
      path = os.path.join(path, "uploads", secure_filename(f.filename))
      f.save(path)
      return "File uploaded successfully"

'''@app.route("/try/<string:name>/", methods=["POST", "GET"])
def tryy(name):
   string = tio.three_in_one(name)
   a = chardet.detect(string.encode("utf-8"))
   #return jsonify({"name":string})
   return json.dumps({"name":string}, ensure_ascii=False)'''

users = {"admin": "12345", "test":"12345"}
diction = {}
lst = []
idx = 0
@app.route("/jishiben/", methods=["POST", "GET"])
def jishiben():
   if "username" in session:
      global lst
      
      path = "c:\\Users\\Jianr\\Desktop\\Application\\"+session["username"]+".txt"
      
      with open(path, "ab+") as input_file:
         try:
            input_file.seek(0)
            lst = pickle.load(input_file)
         except EOFError:
            lst.clear()
      content = request.form
      if request.method=="POST":
         '''try:
            content = request.form
            conn = pymysql.connect("localhost", "root", "123456", "test")
            curs = conn.cursor()         
            curs.execute("INSERT INTO %s VALUES (%s, %s, %s, %s)")
         except:
            conn = pymysql.connect("localhost", "root", "123456", "test")
            curs = conn.cursor()         
            curs.execute("CREATE TABLE %s (id primary key datetime, date varchar(20), event varchar(100), urgency int)")
            curs.execute("INSERT INTO %s VALUES (%s, %s, %s, %s)")'''
         for i in content:
            diction[i] = content[i]
         diction["id"] = idx
         lst.append(diction.copy())
         diction.clear()
         f = open(path,"wb")
         pickle.dump(lst, f)
         f.close()
      return render_template("jishiben.html", content = lst, username = session["username"])
   else:
      return "You  are not logged in to view your jishiben! Please <a href='/loggin'><u>Login</u></a> or <a href='/Register'><u>Register</u></a>.<br>To deactivate your account, click <a href='/Deactivate'><u>here</u></a>.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href='/allusers'><u>view current users</u></a>"

@app.route("/allusers")
def all():
   users = {}
   path = "c:\\Users\\Jianr\\Desktop\\Application\\users.txt"
   with open(path, "ab+") as input_file:
      try:
         conn = pymysql.connect("localhost", "root", "123456", "test")
         curs = conn.cursor()         
         curs.execute("SELECT * FROM users")
         result = curs.fetchall()
      except EOFError:
         conn.rollback()
   #为什么在这里用不了list(dict)?会报错提示list方法没有参数
   #是因为我在后面define了一个没有参数的同名函数list()
   return json.dumps({"users":[i[0] for i in result]}, ensure_ascii=False)+'<br><br><input type="button" value="back" onclick="javascript:window.location.href=\'/jishiben\'" />'

@app.route("/delete/<username>/<idx>")
def delete(username, idx):
   global lst
   lst = [x for x in lst if x["id"] != int(idx)]
   path = "c:\\Users\\Jianr\\Desktop\\Application\\"+username+".txt"
   f = open(path, "wb")
   pickle.dump(lst, f)
   f.close()
   return redirect(url_for("jishiben"))

@app.route("/loggin", methods = ["POST", "GET"])
def loggin():
   users = {}
   path = "c:\\Users\\Jianr\\Desktop\\Application\\users.txt"
   with open(path, "ab+") as input_file:
      try:
         input_file.seek(0)
         users = pickle.load(input_file)
      except EOFError:
         pass
   if request.method=="POST":
      conn = pymysql.connect("localhost", "root", "123456", "test")
      curs = conn.cursor()      
      curs.execute("SELECT * FROM users")
      results = curs.fetchall()
      #if request.form['username'] in users and request.form['password'] == users[request.form['username']]:
      dict_1=dict() 
  
      for name, password in results: 
         dict_1.setdefault(name, password)
      if request.form['username'] in dict_1.keys() and dict_1[request.form['username']] == request.form['password']:
         session["username"] = request.form['username']
         return redirect(url_for("jishiben"))
      else:
         return render_template("log.html", error = "Unauthorized user does not have jishiben.")
   return render_template("log.html")

@app.route("/loggout")
def loggout():
   session.pop("username", None)
   return redirect(url_for("jishiben"))

@app.route("/Register", methods = ["POST", "GET"])
def reg():
   users = {}
   #path = "c:\\Users\\Jianr\\Desktop\\Application\\users.txt"
   '''
   with open(path, "ab+") as input_file:
      try:
         input_file.seek(0)
         users = pickle.load(input_file)
      except EOFError:
         pass
   '''
   if request.method=="POST":
      conn = pymysql.connect("localhost", "root", "123456", "test")
      curs = conn.cursor()         
      curs.execute("INSERT INTO users VALUES (%s,%s)", [request.form["username"], request.form["password"]])
      conn.commit()
      users[request.form["username"]] = request.form["password"]
      #pickle.dump(users, open(path, "wb"))
      #open(os.path.dirname(__file__)+"\\"+request.form["username"]+".txt", "wb")
      return redirect(url_for("jishiben"))
   return render_template("reg.html", url = "Register", mode = "Registration")

@app.route("/Deactivate", methods = ["POST", "GET"])
def deact():
   users = {}
   '''
   path = "c:\\Users\\Jianr\\Desktop\\Application\\users.txt"
   with open(path, "ab+") as input_file:
      try:
         input_file.seek(0)
         users = pickle.load(input_file)
      except EOFError:
         pass
   '''
   if request.method=="POST":     
      try:
         conn = pymysql.connect("localhost", "root", "123456", "test")
         curs = conn.cursor()         
         curs.execute("DELETE FROM users WHERE username=%s and password=%s", [request.form['username'], request.form['password']])
         conn.commit()
         '''
         users.pop(request.form['username'])
         pickle.dump(users, open(path, "wb"))
         os.remove(os.path.dirname(__file__)+"\\"+request.form['username']+".txt")
         '''
         return redirect(url_for("jishiben"))
      except:
         conn.rollback()
         return render_template("reg.html", url = "Deactivate", mode = "Deactivation", error = "Invalid username and/or password")
      finally:
         conn.close()      
   return render_template("reg.html", url = "Deactivate", mode = "Deactivation")

@app.route("/enternew")
def new_student():
   return render_template("stu.html")

@app.route("/addrec", methods=["POST", "GET"])
def addrec():
   if request.method=="POST":
      try:
         nm = request.form["nm"]
         addr = request.form["add"]
         city = request.form["city"]
         pin =request.form["pin"]
         conn = pymysql.connect("localhost", "root", "123456", "test")
         curs = conn.cursor()         
         curs.execute("INSERT INTO students VALUES (default, %s,%s,%s,%s)", [nm,addr,city,int(pin)])
         conn.commit()
         msg = "Record successfully added"
      except:
         conn.rollback()
         msg = "error in insert operation"
      finally:
         conn.close()
         return render_template("re.html", msg = msg)

@app.route("/delerec/<idd>")
def delerec(idd):
   try:
      conn = pymysql.connect("localhost", "root", "123456", "test")
      curs = conn.cursor()
      curs.execute("DELETE FROM students WHERE id = %s", [int(idd)])
      conn.commit()
      msg = "Record successfully deleted"
   except:
      conn.rollback()
      msg = "error in delete operation"
   finally:
      conn.close()
      return render_template("re.html", msg = msg)

@app.route("/list")
def listt():
   conn = pymysql.connect("localhost", "root", "123456", "test")
   curs = conn.cursor()
   curs.execute("SELECT * FROM students")
   results = curs.fetchall()
   js = json.dumps(results)
   return render_template("list.html", rows = results)

@app.route("/home")
def home():
   return render_template("home.html")

if __name__ == '__main__':
   app.run()#host="0.0.0.0", port="80")