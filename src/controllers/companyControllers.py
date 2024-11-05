from flask import redirect, render_template, request, session
from pydantic import ValidationError
from services import companyServices
from validators import CompanyContactForm, CompanyForm, formatErrors

#@refactor and move out of the controller
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
    
def companiesController(groupId):
    if request.method == "GET":
        companies = companyServices.getAllGroupCompanies(groupId)
        return render_template("companies.html", companies=companies)
    
def companyController(id):
    if request.method == "GET":
        company = companyServices.CompanyData()
        if id:
            company = companyServices.getCompany(id)
            if not company:
                return render_template("404.html")
        return render_template("company.html", company=company)
    
#@todo refactor and move out of the controller
def renderCompanyContactTemplate(companyId, contactId, errorMessage=""):
    contact = companyServices.CompanyContactData()
    if companyId and contactId:
        contact = companyServices.getCompanyContact(companyId, contactId)
        if not contact:
            return render_template("404.html")
    return render_template("upsertcontact.html", 
                           companyId=companyId,
                           contactId=contactId,
                           contact=contact,
                           errorMessage=errorMessage)

def upsertCompanyContactController(companyId, contactId):
    if request.method == "GET":
        return renderCompanyContactTemplate(companyId, contactId)
    if request.method == "POST":
        try:
            formData = CompanyContactForm(**request.form.to_dict())
        except ValidationError as e:
            return renderCompanyContactTemplate(companyId, contactId, errorMessage=formatErrors(e.errors()))
        
        if companyServices.upsertCompanyContact(formData, companyId, contactId):
            return redirect(f"/company/{companyId}/contact/{formData.id}")
        return renderCompanyContactTemplate(companyId, contactId, errorMessage="Kontaktin luomisessa tapahtui virhe")
    
def contactController(companyId, contactId):
    if request.method == "GET":
        contact = companyServices.CompanyContactData()
        if contactId and companyId:
            contact = companyServices.getCompanyContact(companyId, contactId)
            if not contact:
                return render_template("404.html")
        return render_template("contact.html", contact=contact)
    
def contactsController(companyId):
    if request.method == "GET":
        contacts = companyServices.getAllCompanyContacts(companyId)
        return render_template("contacts.html", contacts=contacts)