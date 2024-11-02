from app import app
from flask import redirect, render_template, session

from controllers.authControllers import loginController, registerController
from controllers.companyControllers import editCompanyController
from middlware.authMiddlewares import checkSessionAccessToCompanyIdArg

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
@app.route("/editcompany", methods=["GET", "POST"])
@app.route("/editcompany/<int:id>", methods=["GET", "POST"])
@checkSessionAccessToCompanyIdArg()
def editCompany(id=None):
    return editCompanyController(id)

# Custom error routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404