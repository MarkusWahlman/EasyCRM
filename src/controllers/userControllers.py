"""
Controllers for handling user authentication and registration requests.
Includes routes for logging in, registering a new user, and managing users.
Handles form validation and error rendering for login and registration processes.
"""

from flask import redirect, render_template, request, url_for
from pydantic import ValidationError

from validators import UserCreateForm, LoginForm, RegisterForm, UserEditForm, formatErrors
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


def getUserManager(groupId):
    """
    Gets users in the group and renders the user management page.
    """
    users = userServices.getAllGroupUsers(groupId)
    return render_template("usermanager.html", users=users)


def getCreateUser():
    """
    Renders user creation page.
    """
    return render_template('createuser.html')


def postCreateUser(groupId):
    """
    Processes the create user form data and creates a new user.
    Renders the create user page with an error message if user creation fails.
    """
    try:
        formData = UserCreateForm(**request.form.to_dict())
    except ValidationError as e:
        return render_template(
            "createuser.html",
            errorMessage=formatErrors(
                e.errors()))

    if userServices.createUser(formData.username, formData.password, formData.role, groupId):
        return redirect(url_for('userManager'))

    return render_template(
        "createuser.html",
        errorMessage="Käyttäjän luonnissa tapahtui virhe, kokeile toista käyttäjänimeä")


def getEditUser(userId, errorMessage=""):
    """
    Renders user editing page.
    """
    user = userServices.getUser(userId)
    return render_template('edituser.html', user=user, errorMessage=errorMessage)


def postEditUser(groupId, userId):
    """
    Processes the edit user form data and edits a user.
    Renders the edit user page with an error message if user editing fails.
    """
    try:
        formData = UserEditForm(**request.form.to_dict())
    except ValidationError as e:
        return getEditUser(
            userId,
            errorMessage=formatErrors(
                e.errors()))

    if userServices.editUserRole(formData.role, userId, groupId):
        return redirect(url_for('userManager'))
    return getEditUser(userId, errorMessage="Käyttäjän muokkaamisessa tapahtui virhe")


def deleteUser(userId):
    """
    Deletes a user with the given contactId and redirects the user to a relevant valid url
    """
    userServices.deleteUser(userId)

    invalidReferrer = str(userId) in request.referrer
    if request.referrer and not invalidReferrer:
        return redirect(request.referrer)
    return redirect(url_for('usermanager'))
