from flask import redirect, render_template, request, session
from pydantic import ValidationError
from services import companyServices
from validators import CompanyContactForm, CompanyForm, formatErrors

def getUpsertCompany(id):
    return companyServices.renderUpsertCompanyTemplate(id)

def postUpsertCompany(id):
    try:
        formData = CompanyForm(**request.form.to_dict())
    except ValidationError as e:
        return companyServices.renderUpsertCompanyTemplate(id, errorMessage=formatErrors(e.errors()))
    
    companyId = companyServices.upsertCompany(formData, id)
    if not companyId:
        return companyServices.renderUpsertCompanyTemplate(id, 
                                                           errorMessage="Yrityksen luomisessa tapahtui virhe")
    return redirect(f"/company/{companyId}")
   
def getCompanies(groupId):
    if request.method == "GET":
        companies = companyServices.getAllGroupCompanies(groupId)
        return render_template("companies.html", companies=companies)
    
def getCompany(id):
    if request.method == "GET":
        company = companyServices.CompanyData()
        if id:
            company = companyServices.getCompany(id)
            if not company:
                return render_template("404.html")
        return render_template("company.html", company=company)
    
def getUpsertCompanyContact(companyId, contactId):
    return companyServices.renderCompanyContactTemplate(companyId, contactId)
    
def postUpsertCompanyContact(companyId, contactId):
    try:
        formData = CompanyContactForm(**request.form.to_dict())
    except ValidationError as e:
        return companyServices.renderCompanyContactTemplate(companyId, contactId, errorMessage=formatErrors(e.errors()))
    
    contactId = companyServices.upsertCompanyContact(formData, companyId, contactId)
    if not contactId:
        return companyServices.renderCompanyContactTemplate(companyId, 
                                                            contactId, 
                                                            errorMessage="Kontaktin luomisessa tapahtui virhe")
    return redirect(f"/contact/{contactId}")

def getCompanyContact(companyId, contactId):
    contact = companyServices.CompanyContactData()
    if contactId and companyId:
        contact = companyServices.getCompanyContact(companyId, contactId)
        if not contact:
            return render_template("404.html")
    return render_template("contact.html", contact=contact)
    
def getCompanyContacts(companyId):
    if request.method == "GET":
        contacts = companyServices.getAllCompanyContacts(companyId)
        return render_template("contacts.html", contacts=contacts)