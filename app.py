from flask import Flask, render_template, request, session, redirect, url_for, jsonify
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

playerid = 0
level = 1
clue = ""


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
        global playerid
        playerid = record[0]
        global level
        level = record[4]
        # print(level)
        # print(record)
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


@app.route("/signup", methods=["GET", "POST"])
def signup():
    msg = "getting details"
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute(
            "INSERT INTO user(username, email, password) VALUES (%s,%s,%s)",
            (username, email, password),
        )
        record = cursor.fetchone()
        if record:
            return render_template("login.html")
        else:
            return render_template("signup.html")

    return render_template("signup.html")


@app.route("/game", methods=["GET", "POST"])
def game():
    global clue, level
    cursor.execute("SELECT * FROM quesdb WHERE level=%s", ((level - 1),))
    record = cursor.fetchone()
    clue = record[1]
    print("Your Clue is")
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

        if request.form["button"] == "Lake":
            return render_template(
                "cards.html",
                name="https://w0.peakpx.com/wallpaper/751/975/HD-wallpaper-hogwarts-castle-castle-hogwarts.jpg",
                ques=ques,
            )
        if request.form["button"] == "Castle":
            return render_template(
                "cards.html",
                name="https://w0.peakpx.com/wallpaper/290/679/HD-wallpaper-harry-potter-harry-potter-and-the-chamber-of-secrets-hogwarts-castle.jpg",
                ques=ques,
            )
        if request.form["button"] == "Hagrids Hut":
            return render_template(
                "cards.html",
                name="https://images.ctfassets.net/usf1vwtuqyxm/1ERSda92XiUgGWICymMgc6/5f3dff987a43cf997de4b85867bd662f/HagridsHut_WB_F3_BuckbeaksExecutionAtHagridsHut_Illust_100615_Land.jpg?w=914&q=70&fm=webp",
                ques=ques,
            )
        if request.form["button"] == "Hogsmeade Village":
            return render_template(
                "cards.html",
                name="https://static1.srcdn.com/wordpress/wp-content/uploads/2017/04/Harry-Potter-Hogsmeade-at-Christmastime-with-Snow-in-the-air-and-pedestrians.jpg?q=50&fit=crop&w=1500&dpr=1.5",
                ques=ques,
            )
        if request.form["button"] == "Quidditch":
            return render_template(
                "cards.html",
                name="https://i.ytimg.com/vi/uhnvXT9mmyU/maxresdefault.jpg",
                ques=ques,
            )
        # print(record)
        if request.form["button"] == "Room of Requirement":
            if "room" in record:
                print("present")
                return render_template(
                    "cards.html",
                    name="https://static0.gamerantimages.com/wordpress/wp-content/uploads/2022/12/hogwarts-legacy-room-of-requirement-1.jpg?q=50&fit=contain&w=1140&h=&dpr=1.5",
                    ques=ques,
                )
            else:
                print("not present")
                return render_template(
                    "cards.html",
                    name="https://www.pcinvasion.com/wp-content/uploads/2023/02/How-to-make-the-Room-of-Requirement-Bigger-Hogwarts-Legacy-Guide-featured-image.jpg",
                    ques=ques,
                )
        if request.form["button"] == "Dragon Challenge":
            return render_template(
                "cards.html",
                name="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/61c67649-6df5-4fd9-8082-6e4021e6dca5/d2qaz3r-44068af1-e256-4f10-8066-64b36b6abe3e.jpg/v1/fill/w_900,h_600,q_75,strp/the_dragon_fight_by_kaelngu_d2qaz3r-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NjAwIiwicGF0aCI6IlwvZlwvNjFjNjc2NDktNmRmNS00ZmQ5LTgwODItNmU0MDIxZTZkY2E1XC9kMnFhejNyLTQ0MDY4YWYxLWUyNTYtNGYxMC04MDY2LTY0YjM2YjZhYmUzZS5qcGciLCJ3aWR0aCI6Ijw9OTAwIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmltYWdlLm9wZXJhdGlvbnMiXX0.ZgEftWIZeYZZOoX8bx5Qu3_wuy6dahj0WCv701GcSPE",
                ques=ques,
            )
        answer = request.form.get("answer")
        cursor.execute("SELECT ans FROM quesdb WHERE level = %s;", (level,))
        dbans = cursor.fetchone()[0]
        cursor.reset()
        alert_message = "Correct Answer!"
        if answer == dbans:
            level += 1
            cursor.execute("UPDATE user SET level = %s;", (level,))
            connection.commit()
            cursor.execute("SELECT * FROM quesdb WHERE level=%s", ((level - 1),))
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


if __name__ == "__main__":
    app.run(debug=True)
