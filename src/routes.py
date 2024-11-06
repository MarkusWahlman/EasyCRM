from app import app
from flask import redirect, render_template, request, session, url_for

from middlware.authMiddlewares import checkAccessToCompanyIdArg, checkAccessToCompanyAndContactIdArg, checkBelongsToGroup, checkEditAccess

from controllers import companyControllers
from controllers import authControllers

@app.context_processor
def utility_processor():
    def is_active(endpoint):
        return 'active' if request.path == url_for(endpoint) else ''
    return dict(is_active=is_active)

@app.route("/")
def index():
    if not session.get("username"):
        print("NOTTTTTT")
        return redirect("/login")
    return render_template("index.html")

# Authentication routes
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return authControllers.getLogin()
    if request.method == "POST":
        return authControllers.postLogin()
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return authControllers.getRegister()
    if request.method == "POST":
        return authControllers.postRegister()
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# Company routes
@app.route("/company/create", methods=["GET", "POST"])
@app.route("/company/edit/<int:companyId>", methods=["GET", "POST"])
@checkEditAccess()
@checkAccessToCompanyIdArg()
def upsertCompany(companyId=None):
    if request.method == "GET":
        return companyControllers.getUpsertCompany(companyId)
    if request.method == "POST":
        return companyControllers.postUpsertCompany(companyId)

@app.route("/companies", methods=["GET"])
@checkBelongsToGroup()
def companies():
    if request.method == "GET":
        return companyControllers.getCompanies(session.get("groupId"))

@app.route("/company/<int:companyId>", methods=["GET"])
@checkAccessToCompanyIdArg()
def company(companyId):
    if request.method == "GET":
        return companyControllers.getCompany(companyId)

@app.route("/company/<int:companyId>/contact/create", methods=["GET", "POST"])
@app.route("/company/<int:companyId>/contact/edit/<int:contactId>", methods=["GET", "POST"])
@checkEditAccess()
@checkAccessToCompanyAndContactIdArg()
def upsertCompanyContact(companyId, contactId=None):
    if request.method == "GET":
        return companyControllers.getUpsertCompanyContact(companyId, contactId)
    if request.method == "POST":
        return companyControllers.postUpsertCompanyContact(companyId, contactId)

@app.route("/company/<int:companyId>/contact/<int:contactId>", methods=["GET"])
@checkAccessToCompanyAndContactIdArg()
def contact(companyId, contactId):
    if request.method == "GET":
        return companyControllers.getCompanyContact(companyId, contactId)

@app.route("/company/<int:companyId>/contacts", methods=["GET"])
@checkAccessToCompanyIdArg()
def contacts(companyId):
    if request.method == "GET":
        return companyControllers.getCompanyContacts(companyId)

# Custom error routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404