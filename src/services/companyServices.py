"""
Functions for managing company and contact data.
Handles CRUD operations for companies and contacts,
including upserting, retrieving, and displaying data.
"""

from flask import abort, render_template, session
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from db import db


class CompanyData:
    """
    A class representing company data.
    """

    def __init__(
            self,
            companyId=None,
            companyName: str = "",
            businessId: str = "",
            notes: str = "",
            websiteUrl: str = "",
            email: str = "",
            phone: str = "",
            address: str = ""):
        self.companyName = companyName
        self.businessId = businessId
        self.notes = notes
        self.websiteUrl = websiteUrl
        self.email = email
        self.phone = phone
        self.address = address
        self.id = companyId

    id: int
    companyName: str
    businessId: str
    notes: str
    websiteUrl: str
    email: str
    phone: str
    address: str


class CompanyContactData:
    """
    A class representing contact data within a company.
    """

    def __init__(
            self,
            contactId=None,
            firstName: str = "",
            lastName: str = "",
            email: str = "",
            phone: str = "",
            companyName: str = "",
            companyId: str = ""):
        self.id = contactId
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.phone = phone
        self.companyName = companyName
        self.companyId = companyId

    id: int
    firstName: str
    lastName: str
    email: str
    phone: str
    companyName: str
    companyId: str


def renderUpsertCompanyTemplate(companyId, errorMessage=""):
    """
    Render the template for creating or updating a company.
    """
    company = CompanyData()
    if companyId:
        company = getCompany(companyId)
    return render_template("upsertcompany.html",
                           id=companyId,
                           company=company,
                           errorMessage=errorMessage)


def renderCompanyContactTemplate(companyId, contactId, errorMessage=""):
    """
    Render the template for creating or updating a contact in a company.
    """

    contact = CompanyContactData()
    if companyId and contactId:
        contact = getCompanyContact(companyId, contactId)
        if not contact:
            return render_template("404.html")
    return render_template("upsertcontact.html",
                           companyId=companyId,
                           contactId=contactId,
                           contact=contact,
                           errorMessage=errorMessage)


def upsertCompany(company: CompanyData, companyId=None):
    """
    Create or update a company record in the database.
    """

    try:
        if not companyId:
            createCompanySql = text(
                "INSERT INTO companies (companyName, businessId, notes, websiteUrl, email, phone, address, groupId) "
                "VALUES (:companyName, :businessId, :notes, :websiteUrl, :email, :phone, :address, :groupId) "
                "RETURNING id")
            createCompanyResult = db.session.execute(createCompanySql, {
                "companyName": company.companyName,
                "businessId": company.businessId,
                "notes": company.notes,
                "websiteUrl": company.websiteUrl,
                "email": company.email,
                "phone": company.phone,
                "address": company.address,
                "groupId": session["groupId"]
            })
            companyId = createCompanyResult.fetchone()[0]
        else:
            updateCompanySql = text(
                "UPDATE companies SET companyName = :companyName, businessId = :businessId, notes = :notes, "
                "websiteUrl = :websiteUrl, email = :email, phone = :phone, address = :address, groupId = :groupId "
                "WHERE id = :id")
            db.session.execute(updateCompanySql, {
                "companyName": company.companyName,
                "businessId": company.businessId,
                "notes": company.notes,
                "websiteUrl": company.websiteUrl,
                "email": company.email,
                "phone": company.phone,
                "address": company.address,
                "groupId": session["groupId"],
                "id": companyId
            })

        db.session.commit()
        return companyId
    except SQLAlchemyError:
        return None


def getCompany(companyId):
    """
    Retrieve a company by its unique identifier.
    """

    getCompanySql = text("SELECT * FROM companies WHERE id=:id")
    getCompanyResult = db.session.execute(getCompanySql, {"id": companyId})
    company = getCompanyResult.fetchone()
    if not company:
        abort(404)
        return None
    return CompanyData(
        company[0],
        company[1],
        company[2],
        company[3],
        company[4],
        company[5],
        company[6],
        company[7]
    )


def getAllGroupCompanies(groupId, searchString="", showOffset=0):
    """
    Retrieve all companies associated with a specific group, optionally filtered by a substring in the company name.
    """
    getCompaniesSql = "SELECT * FROM companies WHERE groupId=:groupId"

    if searchString:
        getCompaniesSql += r""" AND REGEXP_REPLACE(companyName, '\s', '', 'g') ILIKE REGEXP_REPLACE(:searchString, '\s', '', 'g')"""
        searchString = f"%{searchString}%"

    getCompaniesSql += " OFFSET :showOffset LIMIT 11"

    getCompaniesResult = db.session.execute(
        text(getCompaniesSql), {"groupId": groupId, "searchString": searchString, "showOffset": showOffset} if searchString else {"groupId": groupId, "showOffset": showOffset})
    return [
        CompanyData(
            company[0],
            company[1],
            company[2],
            company[3],
            company[4],
            company[5],
            company[6],
            company[7]
        )
        for company in getCompaniesResult.fetchall()
    ]


def upsertCompanyContact(contact: CompanyContactData, companyId, contactId):
    """
    Create or update a contact record within a company.
    """

    try:
        if not contactId:
            createContactSql = text(
                "INSERT INTO contacts (firstName, lastName, email, phone, companyId) "
                "VALUES (:firstName, :lastName, :email, :phone, :companyId) RETURNING id")
            createContactResult = db.session.execute(createContactSql, {
                "firstName": contact.firstName,
                "lastName": contact.lastName,
                "email": contact.email,
                "phone": contact.phone,
                "companyId": companyId
            })
            contactId = createContactResult.fetchone()[0]
        else:
            updateContactSql = text(
                "UPDATE contacts SET firstName = :firstName, lastName = :lastName, email = :email, phone = :phone "
                "WHERE companyId = :companyId AND id = :contactId")
            db.session.execute(updateContactSql, {
                "firstName": contact.firstName,
                "lastName": contact.lastName,
                "email": contact.email,
                "phone": contact.phone,
                "companyId": companyId,
                "contactId": contactId
            })

        db.session.commit()
        return contactId
    except SQLAlchemyError:
        return None


def getCompanyContact(companyId, contactId):
    """
    Retrieve a contact by its company and contact identifiers.
    """

    getContactSql = text(
        "SELECT * FROM contacts WHERE companyId=:companyId AND id=:contactId")
    getContactResult = db.session.execute(
        getContactSql, {"companyId": companyId, "contactId": contactId})
    contact = getContactResult.fetchone()
    if not contact:
        abort(404)
        return None
    return CompanyContactData(
        contact[0],
        contact[1],
        contact[2],
        contact[3],
        contact[4],
        "",
        companyId
    )


def getAllCompanyContacts(companyId):
    """
    Retrieve all contacts associated with a specific company.
    """

    getContactsSql = text("SELECT * FROM contacts WHERE companyId=:companyId")
    getContactsResult = db.session.execute(
        getContactsSql, {"companyId": companyId})
    return [
        CompanyContactData(
            contact[0],
            contact[1],
            contact[2],
            contact[3],
            contact[4]
        )
        for contact in getContactsResult.fetchall()
    ]


def getAllGroupContacts(groupId, searchString="", showOffset=0):
    """
    Retrieve all contacts associated with a specific group, including their company information.
    """

    getContactsSql = """
        SELECT contacts.*, companies.companyName, companies.id
        FROM contacts
        JOIN companies ON contacts.companyId = companies.id
        JOIN groups ON companies.groupId = groups.id
        WHERE groups.id = :groupId
    """

    if searchString:
        getContactsSql += r"""
            AND REGEXP_REPLACE(CONCAT(contacts.firstName, ' ', contacts.lastName), '\s', '', 'g') ILIKE REGEXP_REPLACE(:searchString, '\s', '', 'g')
        """
        searchString = f"%{searchString}%"

    getContactsSql += " OFFSET :showOffset LIMIT 11"

    getContactsResult = db.session.execute(
        text(getContactsSql), {"groupId": groupId, "searchString": searchString, "showOffset": showOffset} if searchString else {"groupId": groupId, "showOffset": showOffset})

    return [
        CompanyContactData(
            contact[0],  # id
            contact[1],  # firstName
            contact[2],  # lastName
            contact[3],  # email
            contact[4],  # phone
            contact[-2],  # companyName
            contact[-1]  # companyId
        )
        for contact in getContactsResult.fetchall()
    ]

def deleteCompany(companyId):
    """
    Delete a company by its unique identifier.
    """
    try:
        deleteCompanySql = text("DELETE FROM companies WHERE id=:id")
        deleteResult = db.session.execute(deleteCompanySql, {"id": companyId})
        
        if deleteResult.rowcount == 0:
            abort(404)
            return False
        
        db.session.commit()
        return True
    except SQLAlchemyError:
        db.session.rollback()
        return False

def deleteContact(contactId):
    """
    Delete a contact by its unique identifier.
    """
    try:
        deleteContactSql = text("DELETE FROM contacts WHERE id=:id")
        deleteResult = db.session.execute(deleteContactSql, {"id": contactId})
        
        if deleteResult.rowcount == 0:
            abort(404)
            return False
        
        db.session.commit()
        return True
    except SQLAlchemyError:
        db.session.rollback()
        return False