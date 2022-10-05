import ibm_db as db

try:
    conn = db.connect("DATABASE=bludb;HOSTNAME=b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32716;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=xmm71236;PWD=2xTJKfPv4lSkLyqu;", "", "")
    print("Connection successful\n")
	
except:
    print("Error in connection\n")

def showtable():
	print('UNAME\t\t\t\tPASS\t\t\t\tEMAIL\t\t\t\t\t\t\tROLLNO')
	print('-----\t\t\t\t----\t\t\t\t-----\t\t\t\t\t\t\t------\n')
	stmt = db.exec_immediate(conn,"SELECT * FROM USERS")
	dictionary = db.fetch_both(stmt)
	while dictionary!=False:
		print('{}\t\t{}\t\t{}\t\t{}\n'.format(dictionary["UNAME"],dictionary["PASS"],dictionary["EMAIL"],dictionary["ROLLNO"]))
		dictionary = db.fetch_both(stmt)

def insert():
	uname = input("Enter username:")
	password = input("Enter password:")
	email = input("Enter email:")
	rollno = input("Enter rollno:")
	sql = "INSERT INTO users values('{}','{}','{}','{}')".format(uname,password,email,rollno)
	stmt = db.exec_immediate(conn,sql)
	print('The table after insertion:\n')
	showtable()

def update():
	sql = "UPDATE users SET UNAME = 'George' WHERE ROLLNO = 3314" 
	stmt = db.exec_immediate(conn,sql)
	print('The updated table:\n')
	showtable()

def delete():
	sql = "DELETE from users WHERE ROLLNO>3300"
	stmt = db.exec_immediate(conn,sql)
	print('The updated table:\n')
	showtable()

if __name__ == "__main__":
	print("Table USERS:\n")
	showtable()
	insert()
	update()
	delete()
