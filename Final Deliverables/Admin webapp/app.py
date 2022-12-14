from flask import Flask, render_template, request, session, jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from flask_mail import Mail, Message
import os
import ibm_db
import re

# * Object Creation for flask
app = Flask(__name__)
app.secret_key = "a"
app.config["MAIL_SERVER"] = "smtp.sendgrid.net"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "apikey"
app.config["MAIL_PASSWORD"] = os.environ.get("SENDGRID_API_KEY")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

mail = Mail(app)

hostname = "54a2f15b-5c0f-46df-8954-7e38e612c2bd.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
uid = "zsv28701"
pwd = "tf0qA5FpWEJHSoLF"
database = "bludb"
driver = "{IBM DB2 ODBC DRIVER}"
port = "32733"
protocol = "TCPIP"
security = "SSL"
certificate = "DigiCertGlobalRootCA.crt"

try:
    url = (
        "HOSTNAME = {0};"
        "UID = {1};"
        "PWD = {2};"
        "DATABASE = {3};"
        "PORT = {4};"
        "PROTOCOL = {5};"
        "SECURITY = {6};"
        "SSLServerCertificate = {7};"
        "DRIVER = {8};"
    ).format(
        hostname, uid, pwd, database, port, protocol, security, certificate, driver
    )

    conn = ibm_db.connect(url, "", "")
    print(" * Connected to IBM DB")
except:
    print(" * Unable to connect to IBM DB")

# ? Main Routes
# * Route to login
@app.route("/")
@app.route("/login")
def login():
    return render_template("index.html")


# * Route to home
@app.route("/home", methods=["GET", "POST"])
def home():
    msg = ""

    if request.method == "POST":
        username = request.form["UserName"]
        password = request.form["Password"]
        sql = "SELECT * FROM ADMIN WHERE Name = ? AND Password = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session["loggedin"] = True
            session["id"] = account["NAME"]
            session["UserName"] = account["NAME"]
            msg = "Logged in Successfully!"
            return render_template("home.html", user=username)
        else:
            msg = "Incorrect UserName or Password!"
            return render_template("index.html", msg=msg)
    elif "loggedin" in session:
        return render_template("home.html", user=session["UserName"])
    else:
        msg = "Logged out!"
        return render_template("index.html", msg=msg)


# * Route to logout
@app.route("/logout")
def logout():
    session.pop("Loggedin", None)
    session.pop("id", None)
    session.pop("UserName", None)
    return render_template("index.htmL")


# ? User Routes
# * Route to user details manipulation
@app.route("/user")
def user():
    sql = "SELECT * FROM USER"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt)
    userList = []
    while ibm_db.fetch_row(stmt) != False:
        users = {}
        users["UserName"] = ibm_db.result(stmt, 0)
        users["EmailID"] = ibm_db.result(stmt, 1)
        users["PhoneNumber"] = ibm_db.result(stmt, 2)
        userList.append(users)
    return render_template("user.html", users=userList)


# * Route to add new User
@app.route("/new")
def new():
    return render_template("addUser.html")


@app.route("/user/new")
def newUser():
    if request.method == "POST":
        username = request.form["UserName"]
        email = request.form["EmailAddress"]
        phonenumber = request.form["PhoneNumber"]
        password = request.form["Password"]
        sql = "SELECT * FROM USER WHERE Name = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = "Account already exists!"
        elif not re.match(r"[^]", email):
            msg = "Invalid email address"
        elif not re.match(r"[A-Za-z0-9]+", username):
            msg = "Name must contain characters and numbers"
        else:
            insert_sql = "INSERT into USER values (?, ?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, phonenumber)
            ibm_db.bind_param(prep_stmt, 4, password)
            ibm_db.execute(prep_stmt)
            msg = "You have successfully registered"
            return render_template("addUser.html", msg=msg)
    elif request.method == "POST":
        msg = "Please fill out the form"
        return render_template("addUser.html", msg=msg)


@app.route("/zones")
def zones():
    return render_template("zones.html")


@app.route("/zones/add")
def zoneAddPage():
    return render_template("addZone.html")


@app.route("/zones/new", methods=["POST"])
def zoneAdd():
    if request.method == "POST":
        zid = request.form["ZoneID"]
        latitude = request.form["Latitude"]
        longitude = request.form["Longitude"]
        zoneName = request.form["ZoneName"]
        sql = "SELECT * FROM ZONES WHERE ZID = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, zid)
        ibm_db.execute(stmt)
        zone = ibm_db.fetch_assoc(stmt)
        print(zone)
        if zone:
            msg = "Zone already exists!"
        else:
            insert_sql = "INSERT INTO ZONES VALUES (?, ?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, zid)
            ibm_db.bind_param(prep_stmt, 2, latitude)
            ibm_db.bind_param(prep_stmt, 3, longitude)
            ibm_db.bind_param(prep_stmt, 4, zoneName)
            ibm_db.execute(prep_stmt)
            msg = "You have successfully added"
        return render_template("addZone.html", msg=msg)
    elif request.method == "POST":
        msg = "Please fill out the form"
        return render_template("addZone.html", msg=msg)


# * Route to update old zones
@app.route("/zones/update")
def zoneUpdatePage():
    return render_template("updateZone.html")


@app.route("/zones/alter", methods=["POST"])
def zoneAlter():
    if request.method == "POST":
        zid = request.form["ZoneID"]
        latitude = request.form["Latitude"]
        longitude = request.form["Longitude"]
        zoneName = request.form["ZoneName"]
        sql = "SELECT * FROM ZONES WHERE ZID = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, zid)
        ibm_db.execute(stmt)
        zone = ibm_db.fetch_assoc(stmt)
        print(zone)
        if zone:
            update_sql = "UPDATE ZONES SET ZID = ?, Latitude = ?, Longitude = ?, Name = ? WHERE ZID = ?"
            prep_stmt = ibm_db.prepare(conn, update_sql)
            ibm_db.bind_param(prep_stmt, 1, zid)
            ibm_db.bind_param(prep_stmt, 2, latitude)
            ibm_db.bind_param(prep_stmt, 3, longitude)
            ibm_db.bind_param(prep_stmt, 4, zoneName)
            ibm_db.bind_param(prep_stmt, 5, zid)
            ibm_db.execute(prep_stmt)
            msg = "You have successfully added"
        else:
            msg = "Zone not exists!"
        return render_template("updateZone.html", msg=msg)
    elif request.method == "POST":
        msg = "Please fill out the form"
        return render_template("updateZone.html", msg=msg)


# * Route to display all zones
@app.route("/zones/display")
def zoneDisplay():
    sql = "SELECT * FROM ZONES"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt)
    zoneList = []
    while ibm_db.fetch_row(stmt) != False:
        zones = {}
        zones["ZID"] = ibm_db.result(stmt, 0)
        zones["Latitude"] = ibm_db.result(stmt, 1)
        zones["Longitude"] = ibm_db.result(stmt, 2)
        zones["Name"] = ibm_db.result(stmt, 3)
        zoneList.append(zones)
    return render_template("displayZone.html", zones=zoneList)


# * Route to delete old zones
@app.route("/zones/delete")
def zoneDeletePage():
    return render_template("deleteZone.html")


@app.route("/zones/remove", methods=["POST"])
def removeZone():
    msg = ""
    if request.method == "POST":
        zid = request.form["ZoneID"]
        sql = "SELECT * FROM ZONES WHERE ZID = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, zid)
        ibm_db.execute(stmt)
        zone = ibm_db.fetch_assoc(stmt)
        if zone:
            delete_query = "DELETE FROM ZONES WHERE ZID = ?"
            prep_stmt = ibm_db.prepare(conn, delete_query)
            ibm_db.bind_param(prep_stmt, 1, zid)
            ibm_db.execute(prep_stmt)
            msg = "You have successfully deleted."
        else:
            msg = "Sorry! Deletion Failed, Zone not exists."
        return render_template("deleteZone.html", msg=msg)
    elif request.method == "POST":
        msg = "Please fill out the form"
        return render_template("deleteZone.html", msg=msg)


# ? APIs for User App
# * All zone locations
@app.route("/location")
def location():
    sql = "SELECT * FROM ZONES"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt)
    zoneList = []
    while ibm_db.fetch_row(stmt) != False:
        zones = {}
        zones["ZID"] = ibm_db.result(stmt, 0)
        zones["Latitude"] = ibm_db.result(stmt, 1)
        zones["Longitude"] = ibm_db.result(stmt, 2)
        zones["Name"] = ibm_db.result(stmt, 3)
        zoneList.append(zones)
    return jsonify(value=zoneList)


htmlTemplate = ""


@app.route("/getZonesApp")
def returnZonesApp():
    sql = "SELECT * FROM ZONES"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt)
    zoneList = []
    while ibm_db.fetch_row(stmt) != False:
        zones = {}
        zones["ZID"] = ibm_db.result(stmt, 0)
        zones["Latitude"] = ibm_db.result(stmt, 1)
        zones["Longitude"] = ibm_db.result(stmt, 2)
        zones["Name"] = ibm_db.result(stmt, 3)
        zoneList.append(zones)

    print(zoneList)
    return jsonify(zoneList)


# Sendgrid
@app.route("/notify", methods=["POST", "GET"])
def sendMailNotif():
    if request.method == "POST":
        recipient = request.form["recipient"]
        msg = Message("Containment zone alert", recipients=[recipient])
        msg.body = "Containment zone alert!"
        msg.html = (
            "<h1>COVID-19 CONTAINMENT ZONE ALERT</h1>"
            "<p>Warning! You have entered a containment zone. Please be wary of your surroundings.</p>"
        )
        mail.send(msg)
        return "Mail notification sent"
    else:
        return render_template('index.html', msg="404")


# * Run the flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
