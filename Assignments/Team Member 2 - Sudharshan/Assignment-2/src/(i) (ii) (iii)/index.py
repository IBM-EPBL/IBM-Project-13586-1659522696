import os
os.add_dll_directory('C:\Program Files\IBM\clidriver\\bin')

import traceback
import ibm_db
from tabulate import tabulate

class DB2:
    def __init__(self,hostname,uid,pwd,database,driver,port,protocol,security,certificate):
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
            self.conn = ibm_db.connect(creds,"","")
            print("Connected to DB2...")
                
        except:
            traceback.print_exc()
            print("Unable to connect to DB2...")

    def createTable(self):
        query = """
                CREATE TABLE user (
                    username VARCHAR(100) PRIMARY KEY NOT NULL,
                    password VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    rollno INT NOT NULL
                );
                """
        
        try :
            stmt = ibm_db.exec_immediate(self.conn,query)
            print("\nUSER table created...")
        except:
            traceback.print_exc()
            print("Error in table creation...")

    def dropTable(self):
        query = """
                DROP TABLE user;
                """

        try :
            stmt = ibm_db.exec_immediate(self.conn,query)
            print("\nUSER table dropped...")
        except:
            traceback.print_exc()
            print("Error in dropping table...")

    def insertIntoTable(self,username,password,email,rollno):
        query = """
                INSERT INTO USER (username,password,email,rollno)
                VALUES ( 
                """
        query += '\''+username+'\','
        query += '\''+password+'\','
        query += '\''+email+'\','
        query += str(rollno)+');'

        try :
            stmt = ibm_db.exec_immediate(self.conn,query)
            print("\nSuccuessfully inserted...")
        except:
            traceback.print_exc()
            print("Error in insertion...")

    def displayTable(self):
        query = """
                SELECT * FROM USER;
                """
        
        try :
            stmt = ibm_db.exec_immediate(self.conn,query)
            result = []
            tuple = ibm_db.fetch_tuple(stmt)
            
            while tuple != False:
                result.append(list(tuple))
                tuple = ibm_db.fetch_tuple(stmt)

            print("\n---USER TABLE----\n")
            print(tabulate(result,headers=["USERNAME","PASSWORD","EMAIL","ROLLNO"]))

        except:
            traceback.print_exc()
            print("Error in displaying...")

    def updateOrDeleteTable(self,query):
        try :
            stmt = ibm_db.exec_immediate(self.conn,query)
            print("\nTable updated...")
        except:
            traceback.print_exc()
            print("\nError in updating table...")

#DRIVER CODE
hostname = "2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud"
uid = "zxy80489"
pwd = "OCiHNQxQasMfEBDV"
database = "bludb"
driver = "{IBM DB2 ODBC DRIVER}"
port = 30756
protocol = "TCPIP"
security = "SSL"
certificate = "DigiCertGlobalRootCA.crt"

#connecting to db2
db2 = DB2(hostname,uid,pwd,database,driver,port,protocol,security,certificate)

db2.createTable()

db2.insertIntoTable("sudharshan","sk2002","sudharshan.kugan@gmail.com",2019103068)
db2.displayTable()

db2.insertIntoTable("shiva","shiva2002","shiva@gmail.com",2019103059)
db2.displayTable()

db2.insertIntoTable("neeraj","neeg2002","neeraj@gmail.com",2019103041)
db2.displayTable()

query = """
        UPDATE USER SET email = 'kugan.raju@gmail.com'
        WHERE username = 'sudharshan';
        """
db2.updateOrDeleteTable(query)
db2.displayTable()

query = """
        DELETE FROM USER
        WHERE username = 'neeraj';
        """
db2.updateOrDeleteTable(query)
db2.displayTable()

#db2.dropTable()