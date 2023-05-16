from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import mysql.connector
import datetime

connection = mysql.connector.connect(
    host="us-cdbr-east-06.cleardb.net",
    port="3306",
    database="heroku_f8e49261e8690a7",
    user="bcc230d54fe32a",
    password="42fe326e",
)
cursor = connection.cursor()

app = Flask(__name__)
app.secret_key = "super secret key"

playerid = 0
level = 1
clue = ""
email = ""
username = ""
password = ""
prevButton = "default"


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
        # print(level)
        # print(record)
        # print("222222")
        if record:
            session["loggedin"] = True
            session["username"] = record[1]
            # print("Found")
            global playerid
            playerid = record[0]
            global level
            level = record[4]
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
    cursor.execute(
        "SELECT time FROM user WHERE username=%s",
        (username,),
    )
    time = cursor.fetchone()
    return render_template("startpage.html", time=time)


def timedelta_to_seconds(timedelta_obj):
    return int(timedelta_obj.total_seconds())


def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


@app.route("/scorecard", methods=["GET", "POST"])
def scorecard():
    cursor.execute("SELECT * FROM user WHERE level=9 ORDER BY time;")
    records = cursor.fetchall()
    td = []
    name = []
    for i in range(len(records)):
        name.append(records[i][1])
        temp = timedelta_to_seconds(records[i][6])
        td.append(temp)
    time = []
    for i in range(len(td)):
        temp1 = format_time(td[i])
        time.append(temp1)
    return render_template("scorecard.html", time=time, name=name)


@app.route("/userdetail", methods=["GET", "POST"])
def userdetail():
    return render_template("userdetail.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    msg = "getting details"
    if request.method == "POST":
        global email, username, password
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute(
            "INSERT INTO user(username, email, password) VALUES (%s,%s,%s)",
            (username, email, password),
        )
        connection.commit()
        cursor.execute(
            "SELECT * FROM user WHERE username=%s AND password=%s",
            (username, password),
        )
        record = cursor.fetchone()
        # print(record)
        if record:
            return render_template("login.html")
        else:
            return render_template("signup.html")

    return render_template("signup.html")


@app.route("/game", methods=["GET", "POST"])
def game():
    global clue, level
    # if level == 1:
    #     cursor.execute("SELECT * FROM quesdb WHERE level=%s", ((level - 1),))
    # else:
    cursor.execute("SELECT * FROM quesdb WHERE level=%s", ((level),))
    record = cursor.fetchone()
    clue = record[1]
    # print("Your Clue is")
    # print(clue)
    # if request.method == "GET":
    #     answer = request.form["answer"]
    #     print(answer)
    return render_template("game.html", clue=clue, level=level)


@app.route("/cards", methods=["GET", "POST"])
def cards():
    global level, clue
    # print("card called")

    if request.method == "POST":
        cursor.execute("SELECT * FROM quesdb WHERE level=%s", (level,))
        record = cursor.fetchone()
        ques = record[2]
        cursor.reset()
        global prevButton
        if "backbutton" in request.form:
            return render_template("game.html", clue=clue, level=level)
        if "prev-level" in request.form:
            if level == 1:
                alert_message = "You are already on the first level"
                return render_template(
                    "game.html",
                    alert_message=alert_message,
                    clue=clue,
                    level=level,
                )
            level -= 1
            cursor.execute(
                "UPDATE user SET level = %s WHERE userid=%s;",
                (level, playerid),
            )
            connection.commit()
            cursor.execute("SELECT * FROM quesdb WHERE level=%s", ((level),))
            record = cursor.fetchone()
            clue = record[1]
            return render_template("game.html", clue=clue, level=level)
        if "reset" in request.form:
            cursor.execute(
                "UPDATE user SET level = %s, time = %s WHERE userid=%s;",
                (1, 0, playerid),
            )
            connection.commit()
            level = 1
            return render_template("login.html")
        if request.form["button"] == "Lake":
            prevButton = "Lake"
            return render_template(
                "cards.html",
                name="https://w0.peakpx.com/wallpaper/751/975/HD-wallpaper-hogwarts-castle-castle-hogwarts.jpg",
                ques=ques,
            )
        if request.form["button"] == "Castle":
            prevButton = "Castle"
            return render_template(
                "cards.html",
                name="https://w0.peakpx.com/wallpaper/290/679/HD-wallpaper-harry-potter-harry-potter-and-the-chamber-of-secrets-hogwarts-castle.jpg",
                ques=ques,
            )
        if request.form["button"] == "Hagrids Hut":
            prevButton = "Hagrids Hut"
            return render_template(
                "cards.html",
                name="https://images.ctfassets.net/usf1vwtuqyxm/1ERSda92XiUgGWICymMgc6/5f3dff987a43cf997de4b85867bd662f/HagridsHut_WB_F3_BuckbeaksExecutionAtHagridsHut_Illust_100615_Land.jpg?w=914&q=70&fm=webp",
                ques=ques,
            )
        if request.form["button"] == "Hogsmeade Village":
            prevButton = "Hogsmeade Village"
            return render_template(
                "cards.html",
                name="https://static1.srcdn.com/wordpress/wp-content/uploads/2017/04/Harry-Potter-Hogsmeade-at-Christmastime-with-Snow-in-the-air-and-pedestrians.jpg?q=50&fit=crop&w=1500&dpr=1.5",
                ques=ques,
            )
        if request.form["button"] == "Quidditch":
            prevButton = "Quidditch"
            return render_template(
                "cards.html",
                name="https://i.ytimg.com/vi/uhnvXT9mmyU/maxresdefault.jpg",
                ques=ques,
            )
        # print(record)
        if request.form["button"] == "Room of Requirement":
            prevButton = "Room of Requirement"
            # print(prevButton)
            # print("Inside RR")
            if "Alohomora" in record:
                # print("present")
                return render_template(
                    "cards.html",
                    name="https://static0.gamerantimages.com/wordpress/wp-content/uploads/2022/12/hogwarts-legacy-room-of-requirement-1.jpg?q=50&fit=contain&w=1140&h=&dpr=1.5",
                    ques=ques,
                )
            else:
                # print("not present")
                return render_template(
                    "cards.html",
                    name="https://www.pcinvasion.com/wp-content/uploads/2023/02/How-to-make-the-Room-of-Requirement-Bigger-Hogwarts-Legacy-Guide-featured-image.jpg",
                    ques=ques,
                )
        if request.form["button"] == "Dragon Challenge":
            prevButton = "Dragon Challenge"

            if level == 9:
                # cursor.execute("SELECT time FROM user WHERE userid=%s", (playerid,))
                # time = cursor.fetchone()
                return render_template("endpage.html")
            return render_template(
                "cards.html",
                name="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/61c67649-6df5-4fd9-8082-6e4021e6dca5/d2qaz3r-44068af1-e256-4f10-8066-64b36b6abe3e.jpg/v1/fill/w_900,h_600,q_75,strp/the_dragon_fight_by_kaelngu_d2qaz3r-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NjAwIiwicGF0aCI6IlwvZlwvNjFjNjc2NDktNmRmNS00ZmQ5LTgwODItNmU0MDIxZTZkY2E1XC9kMnFhejNyLTQ0MDY4YWYxLWUyNTYtNGYxMC04MDY2LTY0YjM2YjZhYmUzZS5qcGciLCJ3aWR0aCI6Ijw9OTAwIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmltYWdlLm9wZXJhdGlvbnMiXX0.ZgEftWIZeYZZOoX8bx5Qu3_wuy6dahj0WCv701GcSPE",
                ques=ques,
            )
        # if request.form["button-quit"] == "quit":
        #     return render_template("startpage.html")
        if request.form["button"] == "back-button":
            return render_template("game.html", clue=clue, level=level)

        answer = request.form.get("answer")
        cursor.execute("SELECT * FROM quesdb WHERE level = %s;", (level,))
        record = cursor.fetchone()
        dbans = record[4]
        # print(dbans)
        cursor.reset()
        alert_message = "Correct Answer!"
        # print(prevButton)
        # print("mid")
        # print(record[5])
        if answer == dbans and prevButton == record[5]:
            level += 1
            cursor.execute(
                "UPDATE user SET level = %s WHERE userid=%s;",
                (level, playerid),
            )
            connection.commit()
            cursor.execute("SELECT * FROM quesdb WHERE level=%s", ((level),))
            record = cursor.fetchone()
            clue = record[1]
            return render_template(
                "game.html", alert_message=alert_message, clue=clue, level=level
            )
        if answer == dbans:
            print("inside deadend")
            level += 1
            cursor.execute(
                "UPDATE user SET level = %s WHERE userid=%s;",
                (level, playerid),
            )
            connection.commit()
            cursor.execute("SELECT * FROM deadend1 WHERE level=%s", ((1),))
            record = cursor.fetchone()
            clue = record[1]
            return render_template(
                "game.html", alert_message=alert_message, clue=clue, level=level
            )
        alert_message = "Wrong Answer!"
        return render_template(
            "game.html", alert_message=alert_message, clue=clue, level=level
        )

    return render_template("cards.html")


@app.route("/save_timer", methods=["POST"])
def save_timer():
    timer_value = request.form.get("timerValue")
    # print(timer_value)
    # Store the timer value in the database
    cursor.execute(
        "UPDATE user SET time = %s WHERE userid=%s;",
        (timer_value, playerid),
    )
    connection.commit()
    return jsonify({"status": "success"})


@app.route("/rules", methods=["GET", "POST"])
def rules():
    return render_template("rules.html")


if __name__ == "__main__":
    app.run(debug=True)
