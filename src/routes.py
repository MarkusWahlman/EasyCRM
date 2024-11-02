from pydantic import ValidationError
from app import app
from flask import redirect, render_template, request, session

import users
import companies
from validators import CompanyForm, LoginForm, RegisterForm, formatErrors

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        try:
            formData = LoginForm(**request.form.to_dict())
        except ValidationError as e:
            return render_template("login.html", errorMessage=formatErrors(e.errors()))
        
        if users.login(formData.username, formData.password):
            return redirect("/")
        return render_template("login.html", errorMessage="Väärä tunnus tai salasana")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        try:
            formData = RegisterForm(**request.form.to_dict())
        except ValidationError as e:
            return render_template("register.html", message=formatErrors(e.errors()))

        if users.register(formData.username, formData.password):
            return redirect("/")
        return render_template("error.html", "Rekisteröinnissä tapahtui virhe")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/editcompany", methods=["GET", "POST"])
@app.route("/editcompany/<int:id>", methods=["GET", "POST"])
def editcompany(id=None):
    if request.method == "GET":
        return render_template("editcompany.html", id=id)

    if request.method == "POST":
        try:
            formData = CompanyForm(**request.form.to_dict())
        except ValidationError as e:
            return render_template("editcompany.html", errorMessage=formatErrors(e.errors()))

        if companies.upsertCompany(formData, id):
            return redirect("/")
        return render_template("error.html", message="Yrityksen luomisessa tapahtui virhe")