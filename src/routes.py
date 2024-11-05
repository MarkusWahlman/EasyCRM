from app import app
from flask import redirect, render_template, request, session

from controllers.authControllers import getLoginController, postLoginController, getRegisterController, postRegisterController
from controllers.companyControllers import getCompaniesController, getCompanyContactsController, getCompanyController, getCompanyContactController, contactsController, postUpsertCompanyContactController, postUpsertCompanyController, getUpsertCompanyContactController, getUpsertCompanyController
from middlware.authMiddlewares import checkAccessToCompanyIdArg, checkAccessToCompanyAndContactIdArg, checkBelongsToGroup

@app.route("/")
def index():
    return render_template("index.html")

# Authentication routes
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return getLoginController()
    if request.method == "POST":
        return postLoginController()
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return getRegisterController()
    if request.method == "POST":
        return postRegisterController()
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# Company routes
@app.route("/company/create", methods=["GET", "POST"])
@app.route("/company/edit/<int:companyId>", methods=["GET", "POST"])
@checkAccessToCompanyIdArg()
def upsertCompany(companyId=None):
    if request.method == "GET":
        return getUpsertCompanyController(companyId)
    if request.method == "POST":
        return postUpsertCompanyController(companyId)

@app.route("/companies", methods=["GET"])
@checkBelongsToGroup()
def companies():
    if request.method == "GET":
        return getCompaniesController(session.get("groupId"))

@app.route("/company/<int:companyId>", methods=["GET"])
@checkAccessToCompanyIdArg()
def company(companyId):
    if request.method == "GET":
        return getCompanyController(companyId)

@app.route("/company/<int:companyId>/contact/create", methods=["GET", "POST"])
@app.route("/company/<int:companyId>/contact/edit/<int:contactId>", methods=["GET", "POST"])
@checkAccessToCompanyAndContactIdArg()
def upsertCompanyContact(companyId, contactId=None):
    if request.method == "GET":
        return getUpsertCompanyContactController(companyId, contactId)
    if request.method == "POST":
        return postUpsertCompanyContactController(companyId, contactId)

@app.route("/company/<int:companyId>/contact/<int:contactId>", methods=["GET"])
@checkAccessToCompanyAndContactIdArg()
def contact(companyId, contactId):
    if request.method == "GET":
        return getCompanyContactController(companyId, contactId)

@app.route("/company/<int:companyId>/contacts", methods=["GET"])
@checkAccessToCompanyIdArg()
def contacts(companyId):
    if request.method == "GET":
        return getCompanyContactsController(companyId)

# Custom error routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404