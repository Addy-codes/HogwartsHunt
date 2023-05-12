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
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # msg = "Empty"
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cursor.execute(
            "SELECT * FROM user-system WHERE username=%s AND password=%s",
            (username, password),
        )
        record = cursor.fetchone()
        if record:
            session["loggedin"] = True
            session["username"] = record[1]
            return redirect(url_for("index"))
        else:
            msg = "Incorrect username/password.Try again!"
        return render_template("template/login.html")
    return render_template("template/login.html")


if __name__ == "__main__":
    app.run()
