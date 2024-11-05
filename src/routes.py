from app import app
from flask import redirect, render_template, session

from controllers.authControllers import loginController, registerController
from controllers.companyControllers import companiesController, companyController, contactController, contactsController, upsertCompanyContactController, upsertCompanyController
from middlware.authMiddlewares import checkAccessToCompanyIdArg, checkAccessToCompanyAndContactIdArg, checkBelongsToGroup

@app.route("/")
def index():
    return render_template("index.html")

# Authentication routes
@app.route("/login", methods=["GET", "POST"])
def login():
    return loginController()
@app.route("/register", methods=["GET", "POST"])
def register():
   return registerController()
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# Company routes
@app.route("/company/create", methods=["GET", "POST"])
@app.route("/company/edit/<int:companyId>", methods=["GET", "POST"])
@checkAccessToCompanyIdArg()
def upsertCompany(companyId=None):
    return upsertCompanyController(companyId)

@app.route("/companies", methods=["GET"])
@checkBelongsToGroup()
def companies():
    return companiesController(session.get("groupId"))

@app.route("/company/<int:companyId>", methods=["GET"])
@checkAccessToCompanyIdArg()
def company(companyId):
    return companyController(companyId)

@app.route("/company/<int:companyId>/contact/create", methods=["GET", "POST"])
@app.route("/company/<int:companyId>/contact/edit/<int:contactId>", methods=["GET", "POST"])
@checkAccessToCompanyAndContactIdArg()
def upsertCompanyContact(companyId, contactId=None):
    return upsertCompanyContactController(companyId, contactId)

@app.route("/company/<int:companyId>/contacts", methods=["GET"])
@checkAccessToCompanyIdArg()
def contacts(companyId):
    return contactsController(companyId)

@app.route("/company/<int:companyId>/contact/<int:contactId>", methods=["GET"])
@checkAccessToCompanyAndContactIdArg()
def contact(companyId, contactId):
    return contactController(companyId, contactId)

# Custom error routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404