"""
Controllers for handling user authentication and registration requests.
Includes routes for logging in, registering a new user, and managing users.
Handles form validation and error rendering for login and registration processes.
"""

from flask import redirect, render_template, request
from pydantic import ValidationError

from validators import LoginForm, RegisterForm, formatErrors
from services import userServices


def getLogin():
    """
    Renders the login page.
    """
    return render_template("login.html")


def postLogin():
    """
    Processes the login form data and authenticates the user.
    Renders the login page with an error message if authentication fails.
    """
    try:
        formData = LoginForm(**request.form.to_dict())
    except ValidationError as e:
        return render_template(
            "login.html",
            errorMessage=formatErrors(
                e.errors()))

    if userServices.login(formData.username, formData.password):
        return redirect("/")
    return render_template(
        "login.html",
        errorMessage="Väärä tunnus tai salasana")


def getRegister():
    """
    Renders the registration page.
    """
    return render_template("register.html")


def postRegister():
    """
    Processes the registration form data and creates a new user.
    Renders the registration page with an error message if registration fails.
    """
    try:
        formData = RegisterForm(**request.form.to_dict())
    except ValidationError as e:
        return render_template(
            "register.html",
            errorMessage=formatErrors(
                e.errors()))

    if userServices.register(formData.username, formData.password):
        return redirect("/")
    return render_template(
        "register.html",
        errorMessage="Rekisteröinnissä tapahtui virhe, kokeile toista käyttäjänimeä")


def getUserManager():
    """
    Renders the user management page.
    """
    return render_template("usermanager.html")
