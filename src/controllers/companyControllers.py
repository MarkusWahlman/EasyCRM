from flask import redirect, render_template, request, session
from pydantic import ValidationError
from services import companyServices
from validators import CompanyForm, formatErrors

def renderEditCompanyTemplate(id, errorMessage=""):
    company = companyServices.CompanyData()
    if id:
        company = companyServices.getCompany(id)
        if not company:
            return render_template("404.html")
    return render_template("upsertcompany.html", 
                           id=id, 
                           companyName=company.companyName, 
                           businessId=company.businessId, 
                           errorMessage=errorMessage)

def editCompanyController(id):
    if request.method == "GET":
        return renderEditCompanyTemplate(id)

    if request.method == "POST":
        try:
            formData = CompanyForm(**request.form.to_dict())
        except ValidationError as e:
            return renderEditCompanyTemplate(id, errorMessage=formatErrors(e.errors()))

        if companyServices.upsertCompany(formData, id):
            return redirect("/companies")
        return renderEditCompanyTemplate(id, errorMessage="Yrityksen luomisessa tapahtui virhe")
    
def companiesController():
    if request.method == "GET":
        companies = companyServices.getAllCompanies(session.get("groupId"))
        return render_template("companies.html", companies=companies)