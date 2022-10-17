from ssl import CertificateError
import ibm_db
import traceback
from tabulate import tabulate
from flask import Flask, render_template, request
from asyncio.windows_events import NULL

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

def createTable(conn):
    query = """
            CREATE TABLE user (
                username VARCHAR(50) PRIMARY KEY NOT NULL,
                password VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL,
                rollno INT NOT NULL
            );
            """
    
    try :
        stmt = ibm_db.exec_immediate(conn, query)
        print("\nUSER table created")

    except:
        traceback.print_exc()
        print("\nError. Cannot create table")

def insertTable(conn, username, password, email, rollno):
    query = """
            INSERT INTO USER (username,password,email,rollno)
            VALUES ( 
            """
    query += '\''+username+'\','
    query += '\''+password+'\','
    query += '\''+email+'\','
    query += str(rollno)+');'

    try :
        resp = ibm_db.exec_immediate(conn,query)
        print("\nData inserted")
    except:
        traceback.print_exc()
        print("\nError. Cannot insert data")

def displayTable(conn):
    query = """
            SELECT * FROM user;
            """
    try :
        resp = ibm_db.exec_immediate(conn,query)
        result = []
        tuple = ibm_db.fetch_tuple(resp)
        
        while tuple != False:
            result.append(list(tuple))
            tuple = ibm_db.fetch_tuple(resp)

        print("\n\n\t\t\t\t\tUSER TABLE\n\n")
        print(tabulate(result,headers=["USERNAME","PASSWORD","EMAIL","ROLLNO"]))

    except:
        traceback.print_exc()
        print("\nError in displaying")

def dropTable(conn):
    query = """
            DROP TABLE user;
            """
    try :
        stmt = ibm_db.exec_immediate(conn,query)
        print("\nUSER table dropped")
    except:
        traceback.print_exc()
        print("\nError. Cannot drop table")

def updateOrDeleteTable(conn ,query):
    try :
        stmt = ibm_db.exec_immediate(conn, query)
        print("\nTable updated")
    except:
        traceback.print_exc()
        print("\nError. Cannot update table")

if __name__ == "__main__":
    conn = dbconnect()
    createTable(conn)

 #   insertTable(conn, "nk970", "nkpass", "nk.970@gmail.com", 2019103545)
 #   displayTable(conn)

 #   insertTable(conn, "kg234", "kgpass", "kg.234@gmail.com", 2019103873)
 #   displayTable(conn)

 #   query = """
 #       UPDATE USER SET rollno = 2019103546
 #       WHERE username = 'nk970';
 #       """

 #   updateOrDeleteTable(conn, query)
 #   displayTable(conn)
