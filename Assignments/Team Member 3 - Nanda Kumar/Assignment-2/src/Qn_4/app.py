import traceback
import ibm_db
from tabulate import tabulate

from asyncio.windows_events import NULL
from flask import Flask, render_template, request
import os

app = Flask(__name__)

hostname = "b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
uid = "zhw98184"
pwd = "n5oD3WsOV1p53cf1"
database = "bludb"
driver = "{IBM DB2 ODBC DRIVER}"
port = "32716"
protocol = "TCPIP"
security = "SSL"
certificate = "DigiCertGlobalRootCA.crt"

def dbconnect():
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
        conn = ibm_db.connect(creds,"","")
        print("Connected to DB2")
        return conn
            
    except:
        traceback.print_exc()
        print("Unable to connect to DB2")
        return NULL


@app.route('/',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    elif registerUser(request.form['user_name'],
                     request.form['user_password'],
                     request.form['user_email'],
                     request.form['user_rollno']) is True :

        return render_template('login.html', message="Successfully registered!!")
    
    return render_template('register.html', message="User Already exists!!")


def registerUser(username, password, email, rollno):
    conn = dbconnect()

    query = """
            INSERT INTO USER (username,password,email,rollno)
            VALUES ( 
            """
    query += '\''+username+'\','
    query += '\''+password+'\','
    query += '\''+email+'\','
    query += str(rollno)+');'

    try :
        stmt = ibm_db.exec_immediate(conn,query)
        print("\nSuccessfully inserted")
        return True
    except:
        traceback.print_exc()
        print("Error in insertion")
        return False
    
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    elif userExists(request.form['user_name'],
                     request.form['user_password']) is True :

        return render_template('success.html',message=request.form['user_name'])
    
    return render_template('login.html',message="Invalid Credentials!!")

def userExists(username,password):
    conn = dbconnect()

    query = """
            SELECT * FROM USER
            WHERE
            USERNAME = '"""
    query += username + "' and password = '"
    query += password + "';"

    print(query)

    try :
        stmt = ibm_db.exec_immediate(conn,query)
        tuple = ibm_db.fetch_tuple(stmt)
        
        if tuple != False:
            return True
        
        print(tuple)
        return False

    except:
        traceback.print_exc()
        print("Error in displaying")

if __name__ == '__main__':
    app.run(debug=True)