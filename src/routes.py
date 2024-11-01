from app import app
from flask import redirect, render_template, request, session

import users

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print(request.get_data())

    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.login(username, password):
            return redirect("/")
        return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.register(username, password):
            return redirect("/")
        return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")