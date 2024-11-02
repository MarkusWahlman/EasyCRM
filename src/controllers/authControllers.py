from flask import redirect, render_template, request, session
from pydantic import ValidationError

from validators import LoginForm, RegisterForm, formatErrors
from services import userServices

def loginController():
    if request.method == "GET":
            return render_template("login.html")

    if request.method == "POST":
        try:
            formData = LoginForm(**request.form.to_dict())
        except ValidationError as e:
            return render_template("login.html", errorMessage=formatErrors(e.errors()))
        
        if userServices.login(formData.username, formData.password):
            return redirect("/")
        return render_template("login.html", errorMessage="Väärä tunnus tai salasana")

def registerController():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        try:
            formData = RegisterForm(**request.form.to_dict())
        except ValidationError as e:
            return render_template("register.html", errorMessage=formatErrors(e.errors()))

        if userServices.register(formData.username, formData.password):
            return redirect("/")
        return render_template("register.html", "Rekisteröinnissä tapahtui virhe")