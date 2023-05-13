from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    port="3307",
    database="user-system",
    user="root",
    password="qwerty123",
)
cursor = connection.cursor()

app = Flask(__name__)
app.secret_key = "super secret key"


@app.route("/")
def index():
    # if session['loggedin']==True :

    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    msg = "You have been logged in!"
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # print(username)
        # print(password)
        cursor.execute(
            "SELECT * FROM user WHERE username=%s AND password=%s",
            (username, password),
        )
        # print("1111111")
        record = cursor.fetchone()
        # print("222222")
        if record:
            session["loggedin"] = True
            session["username"] = record[1]
            # print("Found")
            return render_template("startpage.html", msg=msg)
        else:
            # print("Not Found")
            msg = "Incorrect username/password.Try again!"
            return render_template("login.html", msg=msg)
    return render_template("login.html")


@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")


@app.route("/startpage", methods=["GET", "POST"])
def startpage():
    return render_template("startpage.html")


@app.route("/scorecard", methods=["GET", "POST"])
def scorecard():
    return render_template("scorecard.html")


@app.route("/userdetail", methods=["GET", "POST"])
def userdetail():
    return render_template("userdetail.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
    msg="getting details"
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute(
            "INSERT INTO user(username, email, password) VALUES (%s,%s,%s)",
            (username, email, password)
        )

        record = cursor.fetchone()
        connection.commit()

        return render_template("login.html")
##        if record:
##            return render_template("login.html")
##       else: 
##           return render_template("signup.html")

        
    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)
