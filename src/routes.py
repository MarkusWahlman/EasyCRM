"""
Defines the routes and controllers for handling user authentication, company management,
and custom error pages. Uses middleware to enforce permissions based on the current
user's group and access levels.
"""

from flask import redirect, render_template, request, session

from middleware.authMiddlewares import (
    checkAccessToCompanyIdArg,
    checkAccessToCompanyAndContactIdArg,
    checkBelongsToGroup,
    checkEditAccess
)
from controllers import companyControllers
from controllers import userControllers

def registerRoutes(app):
    """
    Registers all routes to the provided Flask app instance.
    """
    @app.route("/")
    def index():
        """
        Renders the index page.
        """
        if not session.get("username"):
            return redirect("/login")
        return render_template("index.html")

    # Authentication routes

    @app.route("/login", methods=["GET", "POST"])
    def login():
        """
        Handles user login functionality.
        """
        if request.method == "GET":
            return userControllers.getLogin()
        if request.method == "POST":
            return userControllers.postLogin()
        return render_template('405.html'), 405


    @app.route("/register", methods=["GET", "POST"])
    def register():
        """
        Handles user registration functionality.
        """
        if request.method == "GET":
            return userControllers.getRegister()
        if request.method == "POST":
            return userControllers.postRegister()
        return render_template('405.html'), 405


    @app.route("/logout")
    def logout():
        """
        Logs the user out by clearing the session.
        """
        session.clear()
        return redirect("/")

    # Company routes


    @app.route("/company/create", methods=["GET", "POST"])
    @app.route("/company/edit/<int:companyId>", methods=["GET", "POST"])
    @checkEditAccess()
    @checkAccessToCompanyIdArg()
    def upsertCompany(companyId=None):
        """
        Creates or edits a company based on the request method.
        """
        if request.method == "GET":
            return companyControllers.getUpsertCompany(companyId)
        if request.method == "POST":
            return companyControllers.postUpsertCompany(companyId)
        return render_template('405.html'), 405


    @app.route("/companies", methods=["GET"])
    @checkBelongsToGroup()
    def companies():
        """
        Displays all companies belonging to the user's group.
        """
        if request.method == "GET":
            return companyControllers.getCompanies(session.get("groupId"))
        return render_template('405.html'), 405


    @app.route("/contacts", methods=["GET"])
    @checkBelongsToGroup()
    def contacts():
        """
        Displays all contacts for the user's group.
        """
        if request.method == "GET":
            return companyControllers.getContacts(session.get("groupId"))
        return render_template('405.html'), 405


    @app.route("/company/<int:companyId>", methods=["GET"])
    @checkAccessToCompanyIdArg()
    def company(companyId):
        """
        Displays the details of a specific company.
        """
        if request.method == "GET":
            return companyControllers.getCompany(companyId)
        return render_template('405.html'), 405


    @app.route("/company/<int:companyId>/contact/create", methods=["GET", "POST"])
    @app.route("/company/<int:companyId>/contact/edit/<int:contactId>", methods=["GET", "POST"])
    @checkEditAccess()
    @checkAccessToCompanyAndContactIdArg()
    def upsertCompanyContact(companyId, contactId=None):
        """
        Creates or edits a contact for a company.
        """
        if request.method == "GET":
            return companyControllers.getUpsertCompanyContact(companyId, contactId)
        if request.method == "POST":
            return companyControllers.postUpsertCompanyContact(companyId, contactId)
        return render_template('405.html'), 405


    @app.route("/company/<int:companyId>/contact/<int:contactId>", methods=["GET"])
    @checkAccessToCompanyAndContactIdArg()
    def companyContact(companyId, contactId):
        """
        Displays a specific contact's details for a company.
        """
        if request.method == "GET":
            return companyControllers.getCompanyContact(companyId, contactId)
        return render_template('405.html'), 405


    @app.route("/company/<int:companyId>/contacts", methods=["GET"])
    @checkAccessToCompanyIdArg()
    def companyContacts(companyId):
        """
        Displays all contacts for a specific company.
        """
        if request.method == "GET":
            return companyControllers.getCompanyContacts(companyId)
        return render_template('405.html'), 405


    @app.route("/usermanager", methods=["GET"])
    @checkBelongsToGroup()
    def userManager():
        """
        Displays the user management interface.
        """
        if request.method == "GET":
            return userControllers.getUserManager()
        return render_template('405.html'), 405

    # Custom error routes


    @app.errorhandler(404)
    def pageNotFound():
        """
        Handles 404 errors by rendering a custom 404 error page.
        """
        return render_template('404.html'), 404
