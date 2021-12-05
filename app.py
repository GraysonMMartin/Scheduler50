from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, valid_date

from datetime import datetime, date

app = Flask(__name__)

# Allows changes to show actively instead of restarting flask
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///scheduler50.db")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def home():
    events = db.execute("SELECT * FROM events WHERE id IN (SELECT event_id FROM attendees WHERE person_id = ?)", session["user_id"])
    return render_template("index.html", events=events, user_id=session["user_id"])

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username or username == "":
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password or password == "":
            return apology("must provide password", 400)

        # Ensure password and confirmation match
        elif request.form.get("confirmation") != password:
            return apology("password and confirmation do not match", 400)

        # Ensure the username is not already taken
        if db.execute("SELECT COUNT(username) AS count FROM users WHERE username = ?", username)[0].get("count") != 0:
            return apology("this username is already taken", 400)

        # Add this user to the users table
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))

        # Redirect user to home page
        return redirect("/")

    # GET request
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route("/preferences", methods=["GET", "POST"])
@login_required
def preferences():
    if request.method == "POST":
        return apology("d")
    else:
        return render_template("preferences.html")

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Create a new event"""
    current_id = db.execute("SELECT MAX(id) AS id FROM events WHERE owner_id = ?", session["user_id"])[0].get("id")
    current_event = db.execute("SELECT * FROM events WHERE id = ?", current_id)[0]
    if request.method == "POST":

        title = request.form.get("title")
        start = request.form.get("start_date")
        start_date = start[5:8] + start[8:] + "-" + start[:4]
        end = request.form.get("end_date")
        end_date = end[5:8] + end[8:] + "-" + end[:4]
        description = request.form.get("description")
        location = request.form.get("location")

        #Check that the date is valid
        if not valid_date(start_date,end_date):
          return apology("Please enter a valid date", 403)

        db.execute("INSERT INTO events(title, owner_id, start_date, end_date, description, location) VALUES (?, ?, ?, ?, ?, ?)",
                title, session["user_id"], start_date, end_date, description, location)

        db.execute("INSERT INTO attendees(event_id, person_id, responded) VALUES(?, ?, ?)", current_id, session["user_id"], 0)

        current_invitees = db.execute("SELECT username FROM users WHERE id IN (SELECT person_id FROM attendees WHERE event_id = ?)",
                        current_id)

        return render_template("addinvitees.html", event=current_event, invitees=current_invitees)

    else:
        return render_template("create.html", event = None, current_date = datetime.today().strftime('%Y-%m-%d'))

@app.route("/addinvitees", methods=["POST"])
@login_required
def addinvitees():
    if request.method == "POST":
        guest = db.execute("SELECT id FROM users WHERE username = ?", request.form.get("invitee"))
        if not guest:
            return apology("That username does not exist")
        guest_id = guest[0].get("id")
        current_id = int(request.form.get("event_id"))
        current_event = db.execute("SELECT * FROM events WHERE id = ?", current_id)[0]
        db.execute("INSERT INTO attendees(event_id, person_id, responded) VALUES(?, ?, ?)", current_id, guest_id, 0)
        current_invitees = db.execute("SELECT * FROM users WHERE id IN (SELECT person_id FROM attendees WHERE event_id = ?)",
                        current_id)
        
        return render_template("addinvitees.html", event=current_event, invitees=current_invitees)

@app.route("/removeinvitee", methods=["POST"])
@login_required
def removeinvitee():
    if request.method == "POST":
        guest_id = db.execute("SELECT id FROM users WHERE username = ?", request.form.get("invitee"))[0].get("id")
        current_id = int(request.form.get("event_id"))
        db.execute("DELETE FROM attendees WHERE event_id = ? AND person_id = ?", current_id, guest_id)
        current_event = db.execute("SELECT * FROM events WHERE id = ?", current_id)[0]
        current_invitees = db.execute("SELECT username FROM users WHERE id IN (SELECT person_id FROM attendees WHERE event_id = ?)",
                        current_id)
        return render_template("addinvitees.html", event=current_event, invitees=current_invitees)

@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if request.method == "POST":
        #update event table with new info
        title = request.form.get("title")
        start = request.form.get("start_date")
        start_date = start[5:8] + start[8:] + "-" + start[:4]
        end = request.form.get("end_date")
        end_date = end[5:8] + end[8:] + "-" + end[:4]
        description = request.form.get("description")
        location = request.form.get("location")
        event_id = request.form.get("event_id")

        #Check that the date is valid
        if not valid_date(start_date,end_date):
          return apology("Please enter a valid date", 403)

        db.execute("UPDATE events SET title = ?, start_date = ?, end_date = ?, description = ?, location = ? WHERE id = ?",
                title, start_date, end_date, description, location, event_id)
        # update ateendees
        return redirect("/")
    else:
        event_id = int(request.args.get("event_id"))
        event = db.execute("SELECT * FROM events WHERE id = ?", event_id)
        return render_template("create.html", event=event[0], current_date = datetime.today().strftime('%Y-%m-%d'))


@app.route("/delete_event")
@login_required
def delete_event():
    event_id = int(request.args.get("event_id"))
    db.execute("DELETE FROM attendees WHERE event_id = ?", event_id)
    db.execute("DELETE FROM events WHERE id = ?", event_id)
    return redirect("/")

@app.route("/selecttimes", methods=["GET", "POST"])
@login_required
def selecttimes():
    if request.method == "POST":
        length = request.form.get("length")
        start = request.form.get("start")
        end = request.form.get("end")
        event_id = request.form.get("event_id")

        db.execute("UPDATE events SET length = ?, start_time = ?, end_time = ? WHERE id = ?", length, start, end, event_id)

        events = db.execute("SELECT * FROM events WHERE id IN (SELECT event_id FROM attendees WHERE person_id = ?)", session["user_id"])
        return render_template("index.html", events=events, user_id=session["user_id"])
    else:
        event_id = int(request.args.get("event_id"))
        event = db.execute("SELECT * FROM events WHERE id = ?", event_id)[0]
        return render_template("selecttimes.html", event=event)

@app.route("/set_preferences", methods=["POST"])
@login_required
def set_preferences():
    preferences = request.form.getlist('preferences[]')
    print(preferences)
    return redirect("/")