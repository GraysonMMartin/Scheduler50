from flask import Flask, flash, redirect, render_template, request, session
from cs50 import SQL

app = Flask(__name__)

# Allows changes to show actively instead of restarting flask
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///scheduler50.db")

@app.route("/")
def home():
    return render_template("index.html")