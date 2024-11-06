from flask import abort, redirect, render_template, request, session
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
    
def getContacts(groupId):
    if request.method == "GET":
        contacts = companyServices.getAllGroupContacts(groupId)
        return render_template("contacts.html", contacts=contacts)
    
def getCompany(id):
    if request.method == "GET":
        company = companyServices.CompanyData()
        if id:
            company = companyServices.getCompany(id)
            contacts = companyServices.getAllCompanyContacts(id)
            if not company:
                return render_template("404.html")
        return render_template("company.html", company=company, contacts=contacts)
    
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
    return redirect(f"/company/{companyId}/contact/{contactId}")

def getCompanyContact(companyId, contactId):
    contact = companyServices.CompanyContactData()
    if contactId and companyId:
        contact = companyServices.getCompanyContact(companyId, contactId)
        if not contact:
            abort(404)
    return render_template("companycontact.html", contact=contact, companyId=companyId)
    
def getCompanyContacts(companyId):
    if request.method == "GET":
        contacts = companyServices.getAllCompanyContacts(companyId)
        return render_template("companycontacts.html", contacts=contacts, companyId=companyId)