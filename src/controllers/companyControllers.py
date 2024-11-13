"""
Controllers for handling company-related requests.
Provides routes for upserting companies and company contacts, viewing company and contact details,
and rendering templates related to companies and contacts.
"""

from flask import abort, redirect, render_template, request, url_for
from pydantic import ValidationError
from services import companyServices
from validators import CSRFProtectedForm, CompanyContactForm, CompanyForm, formatErrors


def getUpsertCompany(companyId):
    """
    Renders the upsert company template for the given company ID.
    """

    return companyServices.renderUpsertCompanyTemplate(companyId)


def postUpsertCompany(companyId):
    """
    Processes the request form data, upserts the company, and handles errors.
    Redirects to the company detail page if successful.
    """
    try:
        formData = CompanyForm(**request.form.to_dict())
    except ValidationError as e:
        return companyServices.renderUpsertCompanyTemplate(
            companyId, errorMessage=formatErrors(e.errors()))

    companyId = companyServices.upsertCompany(formData, companyId)
    if not companyId:
        return companyServices.renderUpsertCompanyTemplate(
            companyId, errorMessage="Yrityksen luomisessa tapahtui virhe")
    return redirect(f"/company/{companyId}")


def getCompanies(groupId):
    """
    Renders the filtered companies page with a list of companies for the given group ID.
    """
    searchString = request.args.get('search', "")
    try:
        showOffset = int(request.args.get('showOffset', 0))
        if showOffset < 0:
            showOffset = 0
    except ValueError:
        showOffset = 0
    companies = companyServices.getAllGroupCompanies(
        groupId, searchString, showOffset)
    return render_template("companies.html", companies=companies)


def getContacts(groupId):
    """
    Renders the filtered contacts page with a list of contacts for the given group ID.
    """
    searchString = request.args.get('search', "")
    try:
        showOffset = int(request.args.get('showOffset', 0))
        if showOffset < 0:
            showOffset = 0
    except ValueError:
        showOffset = 0
    contacts = companyServices.getAllGroupContacts(
        groupId, searchString, showOffset)
    return render_template("contacts.html", contacts=contacts)


def getCompany(companyId):
    """
    Renders the company page with company data and contacts for the given ID.
    Displays a 404 page if the company is not found.
    """

    company = companyServices.CompanyData()
    contacts = companyServices.CompanyContactData()
    if companyId:
        company = companyServices.getCompany(companyId)
        contacts = companyServices.getAllCompanyContacts(companyId)
        if not company:
            abort(404)
    return render_template("company.html", company=company, contacts=contacts)


def getUpsertCompanyContact(companyId, contactId):
    """
    Renders the upsert contact page for the given company and possible contact ID.
    """

    return companyServices.renderCompanyContactTemplate(companyId, contactId)


def postUpsertCompanyContact(companyId, contactId):
    """
    Processes the form data, upserts the company contact, and handles errors.
    Redirects to the company contact page if successful.
    """

    try:
        formData = CompanyContactForm(**request.form.to_dict())
    except ValidationError as e:
        return companyServices.renderCompanyContactTemplate(
            companyId, contactId, errorMessage=formatErrors(e.errors()))

    contactId = companyServices.upsertCompanyContact(
        formData, companyId, contactId)
    if not contactId:
        return companyServices.renderCompanyContactTemplate(
            companyId, contactId, errorMessage="Kontaktin luomisessa tapahtui virhe")
    return redirect(f"/company/{companyId}/contact/{contactId}")


def getCompanyContact(companyId, contactId):
    """
    Renders the company contact page with contact data for the given company and contact IDs.
    Displays a 404 page if the contact is not found.
    """

    contact = companyServices.CompanyContactData()
    if contactId and companyId:
        contact = companyServices.getCompanyContact(companyId, contactId)
        if not contact:
            abort(404)
    return render_template(
        "companycontact.html",
        contact=contact,
        companyId=companyId)


def getCompanyContacts(companyId):
    """
    Renders the company contacts page with a list of contacts for the given company ID.
    """

    contacts = companyServices.getAllCompanyContacts(companyId)
    return render_template(
        "companycontacts.html",
        contacts=contacts,
        companyId=companyId)


def deleteCompany(companyId):
    """
    Deletes a company with the given companyId and redirects the user to a relevant valid url
    """
    try:
        CSRFProtectedForm(**request.form.to_dict())
    except ValidationError:
        abort(403)

    companyServices.deleteCompany(companyId)

    invalidReferrer = str(companyId) in request.referrer
    if request.referrer and not invalidReferrer:
        return redirect(request.referrer)
    return redirect(url_for('companies'))


def deleteContact(contactId):
    """
    Deletes a contact with the given contactId and redirects the user to a relevant valid url
    """
    try:
        CSRFProtectedForm(**request.form.to_dict())
    except ValidationError:
        abort(403)

    companyServices.deleteContact(contactId)

    invalidReferrer = str(contactId) in request.referrer
    if request.referrer and not invalidReferrer:
        return redirect(request.referrer)
    return redirect(url_for('contacts'))
