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
                           company=company,
                           errorMessage=errorMessage)

def upsertCompanyController(id):
    if request.method == "GET":
        return renderEditCompanyTemplate(id)

    if request.method == "POST":
        try:
            formData = CompanyForm(**request.form.to_dict())
        except ValidationError as e:
            return renderEditCompanyTemplate(id, errorMessage=formatErrors(e.errors()))
        
        if companyServices.upsertCompany(formData, id):
            return redirect(f"/company/{formData.id}")
        return renderEditCompanyTemplate(id, errorMessage="Yrityksen luomisessa tapahtui virhe")
    
def companiesController():
    if request.method == "GET":
        companies = companyServices.getAllGroupCompanies(session.get("groupId"))
        return render_template("companies.html", companies=companies)
    
def companyController(id):
    if request.method == "GET":
        company = companyServices.CompanyData()
        if id:
            company = companyServices.getCompany(id)
            if not company:
                return render_template("404.html")
        return render_template("company.html", company=company)
    
def upsertCompanyContactController(companyId, contactId):
    if request.method == "GET":
        return render_template("upsertcontact.html")