from asyncio.windows_events import NULL
from flask import Flask, render_template, request
import os
os.add_dll_directory('C:\Program Files\IBM\clidriver\\bin')

import traceback
import ibm_db
from tabulate import tabulate

app = Flask(__name__)

def connectToDB2():
    hostname = "2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud"
    uid = "zxy80489"
    pwd = "OCiHNQxQasMfEBDV"
    database = "bludb"
    driver = "{IBM DB2 ODBC DRIVER}"
    port = 30756
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
        conn = ibm_db.connect(creds,"","")
        print("Connected to DB2...")
        return conn
            
    except:
        traceback.print_exc()
        print("Unable to connect to DB2...")
        return NULL

@app.route('/',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    elif registerUser(request.form['user_name'],
                     request.form['user_password'],
                     request.form['user_email'],
                     request.form['user_rollno']) is True :

        return render_template('login.html',message="Successfully registered!!")
    
    return render_template('register.html',message="User Already exists!!")


def registerUser(username,password,email,rollno):
    conn = connectToDB2()

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
        print("\nSuccuessfully inserted...")
        return True
    except:
        traceback.print_exc()
        print("Error in insertion...")
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
    conn = connectToDB2()

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
        print("Error in displaying...")

if __name__ == '__main__':
  app.run(debug=True)