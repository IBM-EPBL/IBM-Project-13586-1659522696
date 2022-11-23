from flask import Flask, render_template, request
from tabulate import tabulate
from asyncio.windows_events import NULL
import ibm_db as db
import traceback
app = Flask(__name__)
app.static_folder = 'static'

def dbconnect():
    hostname = "b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
    uid = "xmm71236"
    pwd = "2xTJKfPv4lSkLyqu"
    database = "bludb"
    driver = "{IBM DB2 ODBC DRIVER}"
    port = "32716"
    protocol = "TCPIP"
    security = "SSL"
    certificate = "DigiCertGlobalRootCA.crt"

    creds = (
            "HOSTNAME = {0};"
            "UID = {1};"
            "PWD = {2};"
            "DATABASE = {3};"
            "PORT = {4};"
            "PROTOCOL = {5};"
            "SECURITY = {6};"
            "SSLServerCertificate = {7};"
            "DRIVER = {8};"
            ).format(hostname,uid,pwd,database,port,protocol,security,certificate,driver)

    try:
        conn = db.connect(creds,"","")
        print("Connected to DB2...")
        return conn
            
    except:
        traceback.print_exc()
        print("Unable to connect to DB2...")
        return NULL

@app.route("/", methods=['GET','POST'])
def checkUser():
    if request.method == 'GET':
        return render_template("index.html")

    elif registerdata(request.form['username'],
                    request.form['password'],request.form['mail'],request.form['regno']) is True:
                    return render_template("login.html",message="User successfully registered.")
    else:
        return render_template("index.html",message="User already exists!")

@app.route("/signin")
def registerdata(uname,pwd,mail,regno):
    conn = dbconnect()
    sql = "INSERT into users values('{}','{}','{}','{}')".format(uname,pwd,mail,regno)
    try:
        stmt = db.exec_immediate(conn,sql)
        print("data successfully inserted\n")
        return True

    except:
        print("Error in execution")
        return False

@app.route("/login", methods=['GET','POST'])
def checklogin():
    if request.method == 'GET':
        return render_template("login.html")
    elif usercheck(request.form['username'],request.form['password']) is True:
        return render_template("welcome.html")
    else:
        return render_template("login.html",message="User does not exist. Please enter different credentials.")

def usercheck(uname,password):
    conn = dbconnect()
    sql = "SELECT uname,pass from users WHERE uname='{}' and pass='{}'".format(uname,password)
    try:
        data = db.fetch_tuple(db.exec_immediate(conn,sql))
        if data!=False:
            return True
        return False
    except:
        print("Error in fetching\n")
    

if __name__ == '__main__':
    app.run(debug=True)
