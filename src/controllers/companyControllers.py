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

def getUpsertCompanyController(id):
    return renderEditCompanyTemplate(id)

def postUpsertCompanyController(id):
    try:
        formData = CompanyForm(**request.form.to_dict())
    except ValidationError as e:
        return renderEditCompanyTemplate(id, errorMessage=formatErrors(e.errors()))
    
    if companyServices.upsertCompany(formData, id):
        returnPath =  f"/company/{id}"
        if not id:
            returnPath = f"/companies"
        return redirect(returnPath)
    return renderEditCompanyTemplate(id, errorMessage="Yrityksen luomisessa tapahtui virhe")
    
def getCompaniesController(groupId):
    if request.method == "GET":
        companies = companyServices.getAllGroupCompanies(groupId)
        return render_template("companies.html", companies=companies)
    
def getCompanyController(id):
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

def getUpsertCompanyContactController(companyId, contactId):
    return renderCompanyContactTemplate(companyId, contactId)
    
def postUpsertCompanyContactController(companyId, contactId):
    try:
        formData = CompanyContactForm(**request.form.to_dict())
    except ValidationError as e:
        return renderCompanyContactTemplate(companyId, contactId, errorMessage=formatErrors(e.errors()))
    
    if companyServices.upsertCompanyContact(formData, companyId, contactId):
        returnPath =  f"/company/{companyId}"
        if contactId:
            returnPath += f"/contact/{contactId}"
        return redirect(returnPath)
    return renderCompanyContactTemplate(companyId, contactId, errorMessage="Kontaktin luomisessa tapahtui virhe")

def getCompanyContactController(companyId, contactId):
    contact = companyServices.CompanyContactData()
    if contactId and companyId:
        contact = companyServices.getCompanyContact(companyId, contactId)
        if not contact:
            return render_template("404.html")
    return render_template("contact.html", contact=contact)
    
def getCompanyContactsController(companyId):
    if request.method == "GET":
        contacts = companyServices.getAllCompanyContacts(companyId)
        return render_template("contacts.html", contacts=contacts)